from concurrent.futures import ThreadPoolExecutor

class ThreadPool:
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, func, *args, **kwargs):
        future = self.executor.submit(func, *args, **kwargs)
        return future

    def shutdown(self):
        self.executor.shutdown(wait=True)