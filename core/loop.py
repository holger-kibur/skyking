import time

class BaseLoopJob(object):
    def __init__(self, interval):
        self.last_time = None
        self.interval = interval
        self.close_signal = False

    def init(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def close(self):
        self.close_signal = True

class MainLoop(object):
    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def loop(self):
        any_closers = False
        while not any_closers:
            now_time = time.time()
            for job in self.jobs:
                if job.last_time is None:
                    job.init()
                    job.run()
                    job.last_time = now_time
                elif now_time - job.last_time >= job.interval:
                    job.run()
                    job.last_time = now_time
            for job in self.jobs:
                any_closers = any_closers or job.close_signal
            time.sleep(0.01)
        for job in self.jobs:
            if not job.close_signal:
                job.close()
