class Worker:
    def __init__(self): self.jobs = []
    def add_job(self, j): self.jobs.append(j)
    def run(self): return self.jobs.pop(0) if self.jobs else None
