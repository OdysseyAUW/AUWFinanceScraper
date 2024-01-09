import time

class RateLimiter:
    def __init__(self, max_calls, per_seconds):
        self.calls = []
        self.max_calls = max_calls
        self.per_seconds = per_seconds

    def wait(self):
        while len(self.calls) >= self.max_calls:
            if time.time() - self.calls[0] > self.per_seconds: self.calls.pop(0)
            else: time.sleep(0.1)

    def add_call(self): self.calls.append(time.time())
    def reset(self): self.calls = []