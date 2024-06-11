import logging
from rq import Queue

import lib.api_clients as api_clients
from lib.browser_pool import create_placeholder

class GlobalState():
    def __init__(self):

        self.redis = api_clients.get_redis()
        self.job_queue = Queue("jvoy", connection=self.redis, default_timeout=-1)

        # self.xvfb_placeholder = create_placeholder()
        self.logger = logging.getLogger(__name__)

        self.es = api_clients.get_elastic()