import os
import random
import subprocess
from pathlib import Path
from time import sleep
from typing import cast

from selenium import webdriver

import lib.api_clients as api_clients

redis = api_clients.get_redis()


BROWSER_POOL_NAME = "browser:ports"
BROWSER_PORT_RANGE_START = 9000

XDISPLAY_POOL_NAME = "browser:xdisplay"
XDISPLAY_RANGE_START = 1

REDIS_LOCK_KEY = "environment_modification_lock"

# anything with os.environ / DISPLAY needs to be locked


class display_lock:
    """
    context manager for locked resource os.environ display across threads
    will lock os.environ if unheld, otherwise wait a random amount of time and retry

    usage:

    with display_lock(":1") as lock:
        do_something_that_needs_DISPLAY_set()

    >> valid


    accidentally locking for the same display while holding that lock is a no-op:

    with display_lock(":1") as lock_a:
        with display_lock(":1") as lock_b:
            do_something_that_needs_DISPLAY_set()

    >> valid, holds :1


    holding a lock and attempting to set a different display is INVALID usage:

    with display_lock(":1") as lock_a:
        with display_lock(":2") as lock_b:
            function()

    >> fails
    """

    def __init__(self, display):
        self.display = display
        self.redundant_inner_lock = False

    def __enter__(self):
        print("attempting to lock DISPLAY", flush=True)

        lock = redis.get(REDIS_LOCK_KEY)
        if redis.get(REDIS_LOCK_KEY) == self.display:
            print("\talready holding lock on same display, no-op", flush=True)
            self.redundant_inner_lock = True
            return self

        while lock is not None:
            print(f"\tlock currently held by {lock}", flush=True)
            wait_time = random.uniform(1, 5)
            sleep(wait_time)
            lock = redis.get(REDIS_LOCK_KEY)

        redis.set(REDIS_LOCK_KEY, self.display)
        os.environ["DISPLAY"] = self.display
        print(f"\tlocked DISPLAY to {self.display}", flush=True)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("attempting to unlock DISPLAY", flush=True)
        if self.redundant_inner_lock:
            print("\tlock was redundant, no-op")
            return
        if redis.get(REDIS_LOCK_KEY) is None:
            print("\tnot currently locked. this should never happen.")
            return
        redis.delete(REDIS_LOCK_KEY)
        print("\tsuccessfully unlocked", flush=True)


# for pyautogui import-time constraint before use -- see DISPLAY in docker-compose.yaml
def create_placeholder():
    print("executed", flush=True)
    try:
        os.remove("/tmp/.X99-lock")
    except Exception:
        pass
    redis.sadd(XDISPLAY_POOL_NAME, ":99")
    subprocess.Popen(
        ['touch ~/.Xauthority && xvfb-run -n99 -s "-ac" -- xterm'],
        shell=True,
        preexec_fn=os.setsid,
    )
    print(":99 placeholder started to work around pyautogui import-time", flush=True)


def active_clients() -> dict[str, int]:
    return {
        "ports": cast(int, redis.scard(BROWSER_POOL_NAME)),
        "x11_displays": cast(int, redis.scard(XDISPLAY_POOL_NAME)),
    }


def reserve_lowest_unused_port() -> int:
    port = BROWSER_PORT_RANGE_START
    while redis.sismember(BROWSER_POOL_NAME, str(port)):
        port += 1
    redis.sadd(BROWSER_POOL_NAME, str(port))
    print(f"reserved port {port}", flush=True)
    return port


def release_port(port: int):
    print(f"released port {port}", flush=True)
    redis.srem(BROWSER_POOL_NAME, str(port))


def reserve_lowest_unused_display() -> str:
    num = XDISPLAY_RANGE_START
    while redis.sismember(XDISPLAY_POOL_NAME, f":{num}"):
        num += 1
    redis.sadd(XDISPLAY_POOL_NAME, f":{num}")
    print(f"reserved display :{num}", flush=True)
    return f":{num}"


def release_display(display: str):
    print(f"released display {display}", flush=True)
    redis.srem(XDISPLAY_POOL_NAME, display)


# TODO: no clear to move forward on a set download dir yet.
def module_root_download_dir(display: str) -> Path:
    return Path(__file__).parent.parent / "downloads"


class spawn_browser:
    """
    context manager for spawning browsers to run tasks in, managing x displays and resources
    `with spawn_browser() as browser:`
        will spawn a chromium process with remote debugging;
    `with spawn_browser(selenium=True) as browser:`
        will spawn a chromedriver process with remote debugging and return the handle of the selenium driver in the object;
    stored xdisplay info and other details are handled by redis.
    """

    # TODO: firefox?

    port: int
    display: str
    selenium: bool
    browser: subprocess.Popen | None
    driver: webdriver.Chrome | None
    driver_fb: subprocess.Popen | None

    chromium_flags = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        # shell=True lets us get away with this -- needed for parallel
        # https://askubuntu.com/questions/35392/how-to-launch-a-new-instance-of-google-chrome-from-the-command-line
        "--user-data-dir=$(mktemp -d)",
    ]

    def __init__(self, resolution: tuple[int, int], selenium: bool = False):
        self.selenium = selenium
        self.resolution = resolution
        self.driver = None

    def spawn_chromium(self):
        resolution = f"{self.resolution[0]}x{self.resolution[1]}"
        launch_string = " ".join(
            [
                "touch ~/.Xauthority",
                "&&",
                f'xvfb-run -s "-ac -screen 0 {resolution}x24"',
                f"-n{self.display[1:]}",
                "chromium",
                " ".join(self.chromium_flags),
            ]
        )
        print(launch_string, flush=True)
        self.browser = subprocess.Popen([launch_string], shell=True, preexec_fn=os.setsid)
        return self

    def spawn_chromedriver(self):
        self.spawn_chromium()
        sleep(5)
        options = webdriver.ChromeOptions()
        options.debugger_address = "127.0.0.1:" + str(self.port)
        self.driver = webdriver.Chrome(options=options)
        print("spawned driver", flush=True)
        return self

    def __enter__(self):
        self.port = reserve_lowest_unused_port()
        self.display = reserve_lowest_unused_display()
        with display_lock(self.display):
            os.environ["DISPLAY"] = self.display
            self.chromium_flags += [
                f"--window-size={self.resolution[0]},{self.resolution[1]}",
                "--window-position=0,0",
                f"-remote-debugging-port={self.port}",
                f"--remote-allow-origins=http://127.0.0.1:{self.port}",
            ]
            if self.selenium:
                self.spawn_chromedriver()
            else:
                self.spawn_chromium()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.selenium:
            if self.driver is not None:
                self.driver.quit()
        # not an elif here: this is for both.
        if self.browser is not None:
            self.browser.kill()
            os.killpg(os.getpgid(self.browser.pid), 9)
            self.browser.wait()
            self.browser.communicate()
            self.browser = None
        release_port(self.port)
        release_display(self.display)
        try:
            os.remove(f"/tmp/{self.display[:1]}.X-lock")
        except Exception:
            pass
        if exc_type:
            print(exc_tb)
            raise Exception()
