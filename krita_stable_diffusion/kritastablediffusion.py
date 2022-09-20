import sys
import queue
sys.path.append("/home/joe/Projects/ai/krita_stable_diffusion")

import logger as log
from connect import StableDiffusionRequestQueueWorker


class StableDiffusionConnectionManager:
    def stop_stable_diffusion(self):
        # stop the stablediffusion runner
        pass

    def start_request_connection(self):
        # self.request_worker.start()
        pass

    def stop_request_connection(self):
        # self.request_worker.stop()
        pass

    def restart_request_connection(self):
        # self.request_worker.restart()
        pass

    def start_response_connection(self):
        # self.request_worker.start()
        pass

    def stop_response_connection(self):
        # self.request_worker.stop()
        pass

    def restart_response_connection(self):
        # self.request_worker.restart()
        pass

    def start_request_worker(self):
        self.request_worker.start()

    def stop_request_worker(self):
        self.request_worker.stop()

    def restart_request_worker(self):
        self.request_worker.restart()

    def start_response_worker(self):
        self.response_worker.start()

    def stop_response_worker(self):
        self.response_worker.stop()

    def restart_response_worker(self):
        self.response_worker.restart()

    def start(self):
        """
        Start all connections and workers
        :return: None
        """
        self.start_request_connection()
        self.start_response_connection()
        self.start_request_worker()
        self.start_response_worker()

    def stop(self):
        """
        Stop all connections and workers
        :return: None
        """
        self.stop_request_connection()
        self.stop_response_connection()
        self.stop_request_worker()
        self.stop_response_worker()

    def restart(self):
        """
        Restart all connections and workers
        :return: None
        """
        self.restart_request_connection()
        self.restart_response_connection()
        self.restart_request_worker()
        self.restart_response_worker()

    def __init__(self, *args, **kwargs):
        """
        Initialize all connections and workers
        """
        # create queues
        self.request_queue = kwargs.get("request_queue", queue.SimpleQueue())
        self.response_queue = kwargs.get("response_queue", queue.SimpleQueue())

        # create request worker thread which
        # 1. waits for messages on the request_queue
        # 2. sends the request to stable diffusion
        # 3. adds the response to the response_queue
        log.info("creating request worker...")
        self.request_worker = StableDiffusionRequestQueueWorker(
            port=50006
        )

        # create response worker thread which
        # 1. waits for messages on the response_queue
        # 2. sends the response to the client
        # log.info("creating response worker...")
        # self.response_worker = StableDiffusionResponseQueueWorker(
        #     port=50007,
        #     queue=self.response_queue,
        #     callback=callback
        # )

        # # # create request connection thread
        # log.info("creating request connection...")
        # self.request_connection = SimpleEnqueueSocketClient(
        #     port=50006,
        #     queue=self.request_queue,
        #     worker=self.request_worker
        # )
        #
        # # create response connection thread
        # log.info("creating response connection...")
        # self.response_connection = SimpleEnqueue(
        #     queue=self.response_queue,
        #     worker=self.response_worker
        # )

if __name__ == "__main__":
    # _txt2img_loader = Txt2Img(
    #     options=SCRIPTS["txt2img"],
    #     model=None,
    #     device=None
    # )
    StableDiffusionConnectionManager()
