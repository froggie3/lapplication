import collections
import dataclasses
import time

from .base import Base


class TimerResult(Base):
    """
    A dedicated class to store / show the time taken
    """

    def __init__(self, seconds: float) -> None:
        self.seconds = seconds

    def __repr__(self):
        return self.__class__.__name__ + f"({self.express()})"

    def __str__(self):
        return self.express()

    def express(self) -> str:
        minutes, remainder = divmod(self.seconds, 60)
        seconds = round(remainder, 3)
        return "{:02d}:{:06.3f}".format(int(minutes), seconds)


TimeExpr = TimerResult | float


@dataclasses.dataclass
class _Lap:
    label: str
    second: TimeExpr


class _Laps(Base):
    _laps: list[_Lap]

    def __init__(self):
        self._laps = []

    def __getitem__(self, index):
        return self._laps[index]

    def append(self, second: TimeExpr, note: str | None = None):
        _elapsed_sec = None
        if isinstance(second, float):
            _elapsed_sec = TimerResult(second)
        elif isinstance(second, TimerResult):
            _elapsed_sec = second
        else:
            raise TypeError

        lap_number: int = len(self._laps)
        lap_label = "lap" if note is None else str(note)
        lap_data = _Lap(f"{lap_label} #{lap_number:02d}", _elapsed_sec)

        self._laps.append(lap_data)


class Timer(Base):
    """
    A dedicated class to measure the time taken in execution of a function
    """

    def __init__(self) -> None:
        self._elapsed = 0.0
        self._started = 0.0
        self.laps = _Laps()

        self._window_length = 10
        self._window = collections.deque([])

    @property
    def elapsed(self):
        return time.time() - self._started

    @property
    def started(self):
        return self._started

    def start(self) -> "Timer":
        self._started = time.time()
        return self

    def stop(self) -> "Timer":
        self.lap()
        return self

    def lap(self, note: str | None = None) -> TimerResult:
        _elapsed_sec = TimerResult(self.elapsed)
        self.laps.append(_elapsed_sec, note)
        lap_data = self.laps[-1]

        return lap_data

    def execute(self, user_function) -> "Timer":
        user_function()
        return self

    def retrieve_result(self) -> TimerResult:
        return TimerResult(self._elapsed)
