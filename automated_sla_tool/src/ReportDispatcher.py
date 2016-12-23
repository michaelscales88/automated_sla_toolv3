from concurrent.futures import ThreadPoolExecutor, as_completed
from automated_sla_tool.src.FinishedDecorator import FinishedDecorator as check_running


class ReportDispatcher(object):
    running = False

    @check_running(running)
    def __init__(self, pool_size=5):
        super().__init__()
        self._max_size = pool_size
        self._jobs = {}
        self._inc_jobs = []
        self._in_proc = {}
        ReportDispatcher.running = True

    def listener(self, jobs):
        for job in as_completed(jobs):
            task_name = self._jobs[job]
            self._in_proc[task_name].data = job.result()
            del self._jobs[job]
            self._in_proc.pop(task_name)

    def submit_job(self, inc_job):
        self._inc_jobs.append(inc_job)

    def dispatch(self):
        with ThreadPoolExecutor(max_workers=self._max_size) as executor:
            for next_job in reversed(self._inc_jobs):
                job = executor.submit(fn=next_job.target,
                                      day=next_job.day)
                self._jobs[job] = next_job.day
                self._in_proc[next_job.day] = self._inc_jobs.pop(-1)
            self.listener(self._jobs)

    def print_inproc(self):
        print(self._in_proc)
