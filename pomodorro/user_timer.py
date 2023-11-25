import time

from micropython import const

MINUTES_25 = const(60 * 25)
MINUTES_15 = const(60 * 15)
MINUTES_5 = const(60 * 5)


class Timer:
    def __init__(self, duration=0.0):
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
        self._time_paused = 0
        self._paused = False
        self._time_start = self._time_func
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
        self._paused = True

    def resume(self):
        if not self._paused:
            return
        self._paused = False
        pause_duration = self._time_func - self._time_paused
        self._time_start += pause_duration
        self._expire_time += pause_duration


class Pomodoro(Timer):
    focus_duration = MINUTES_25
    short_break_duration = MINUTES_5
    long_break_duration = MINUTES_15

    def __init__(self):
        super().__init__(self.focus_duration)
        self.focus_time = True
        self.count = 0

    def next(self):
        if self.focus_time:
            self.count += 1

        self.focus_time = not self.focus_time

        if self.focus_time:
            self.duration = self.focus_duration
        elif self.count % 4:
            self.duration = self.short_break_duration
        else:
            self.duration = self.long_break_duration

        self.reset()
