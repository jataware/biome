import time
import requests

BASE_URL = "http://vpnrotate:8080"


class VPNManager:
    unused: dict[str, set[str]]
    blocked: dict[str, set[str]]
    selected: tuple[str, str] | None

    def __init__(self) -> None:
        self.unused = {}
        self.selected = None

    def handle_api_error(self, response: requests.Response, exception_text: str) -> None:
        if response.status_code != 200:
            raise Exception(
                f"{exception_text}. {response.status_code}: {response.content}"
            )

    def initialize(self) -> None:
        if self.selected is not None:
            return

        response = requests.post(f"{BASE_URL}/vpn/configs")
        self.handle_api_error(response, "failed to update vpn configs")

        response = requests.get(f"{BASE_URL}/vpns")
        self.handle_api_error(response, "failed to fetch list of vpns")
        vpns_list = response.json()
        for provider, server_list in vpns_list.items():
            self.unused[provider] = set(server_list)

        num_servers = [len(self.unused[provider]) for provider in self.unused.keys()]
        if sum(num_servers) == 0:
            raise Exception(
                "failed to get any available vpns - halting. check environment variable to see if they are properly set for jataware/vpnrotate container"
            )
        available_servers = list(zip(self.unused.keys(), num_servers))
        print(f"vpnrotate: initialized pool: {available_servers}", flush=True)
        self.cycle()

    def cycle(self) -> None:
        providers = [
            provider for provider in self.unused.keys() if len(self.unused[provider]) != 0
        ]

        # if all vpns have been used and blocked at some point, re-seed the pool
        if len(providers) == 0:
            self.selected = None
            self.initialize()
            return

        provider = providers.pop()
        server = self.unused[provider].pop()

        print(f"attempting to connect to {provider} {server}", flush=True)
        response = requests.post(f"{BASE_URL}/vpn/start")
        self.handle_api_error(response, "failed to start")

        response = requests.put(
            f"{BASE_URL}/vpn/restart", json={"vpn": provider, "server": server}
        )
        self.handle_api_error(response, f"failed to connect to {provider} {server}")

        response = requests.get(f"{BASE_URL}/vpnsecure")
        while bytes.decode(response.content, "utf-8") != "true":
            print("\tvpn not initialized yet. retrying in 3...", flush=True)
            time.sleep(3)
            response = requests.get(f"{BASE_URL}/vpnsecure")

        print(f"securely connected to {provider} {server}", flush=True)

        self.selected = (provider, server)
