import time


class Timer:
    def __init__(self, duration=0):
        self._duration = duration
        self.reset()

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if duration < 0:
            raise ValueError("duration must be positive")
        self._duration = duration

    @property
    def remaining(self):
        return self._expire_time - self._time_func

    @property
    def elapsed(self):
        return self._time_func - self._time_start

    @property
    def is_expired(self):
        return self.remaining <= 0

    @property
    def _time_func(self):
        if self._paused:
            return self._time_paused
        return time.monotonic()

    def reset(self):
        self._time_start = time.monotonic()
        self._time_paused = 0
        self._paused = False
        self._expire_time = self._time_start - 1

    def start(self):
        if self._paused:
            self.resume()
        self._time_start = self._time_func
        self._expire_time = self._time_start + self._duration

    def pause(self):
        if self._paused:
            return
        self._time_paused = self._time_func

    def resume(self):
        if not self._paused:
            return
        pause_duration = self._time_func - self._time_paused
        self._time_start += pause_duration
        self._expire_time += pause_duration
        self._paused = False
