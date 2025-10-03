from __future__ import annotations
from datetime import datetime, timedelta

class SystemTimeProvider:
    def now(self) -> datetime:
        return datetime.now()

class FakeTimeProvider:
    def __init__(self, start: datetime):
        self._current = start

    def now(self) -> datetime:
        return self._current

    def advance(self, *, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0) -> None:
        delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        self._current += delta
