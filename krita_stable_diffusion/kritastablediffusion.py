import os
import sys
import queue
import threading
import time

HOME = os.path.expanduser("~")
sys.path.append(f"{HOME}Projects/ai/krita_stable_diffusion")

import logger as log
from connect import StableDiffusionRequestQueueWorker


class StableDiffusionConnectionManager:
    def __init__(self, *args, **kwargs):
        """
        Initialize all connections and workers
        """
        # create queues
        self.request_queue = kwargs.get("request_queue", queue.SimpleQueue())
        self.response_queue = kwargs.get("response_queue", queue.SimpleQueue())

        # create request client
        log.info("creating request worker...")
        self.request_worker = StableDiffusionRequestQueueWorker(
            port=50006,
            pid=kwargs.get("pid"),
        )

if __name__ == "__main__":
    # get pid from command line
    pid = sys.argv[2]
    # clear sys.argv
    sys.argv = sys.argv[:1]
    StableDiffusionConnectionManager(pid=pid)
