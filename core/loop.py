import time

class BaseLoopJob(object):
    def __init__(self, interval, **kwargs):
        self.last_time = None
        self.interval = interval
        self.signal_close = False

    def init(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

class MainLoop(object):
    def __init__(self):
        self.jobs = []

    def loop(self):
        any_closers = False
        while not any_closers:
            now_time = time.time()
            for job in self.jobs:
                if job.last_time is None:
                    job.init()
                    job.run()
                elif now_time - job.last_time >= job.interval:
                    job.run()
                job.last_time = now_time
            for job in self.jobs:
                any_closers = any_closers and job.signal_close
        for job in self.jobs:
            job.close()
