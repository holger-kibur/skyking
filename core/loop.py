import time

class BaseLoopJob(object):

    cron_inst = None

    def __init__(self, interval):
        self.last_time = None
        self.interval = interval
        self.close_signal = False

    def init(self):
        pass

    def run(self):
        pass

    def close(self):
        self.close_signal = True

    def add_self_to_cron(self):
        BaseLoopJob.cron_inst.add_job(self)

    def del_self_from_cron(self):
        BaseLoopJob.cron_inst.del_job(self)

class MainLoop(object):
    def __init__(self):
        self.jobs = []
        BaseLoopJob.cron_inst = self

    def add_job(self, job):
        self.jobs.append(job)

    def del_job(self, job):
        for i in range(len(self.jobs))[::-1]:
            if self.jobs[i] is job:
                self.jobs.pop(i)
                break

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
