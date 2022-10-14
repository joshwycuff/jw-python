# std
from __future__ import annotations as _annotations
from enum import Enum as _Enum


class Level(_Enum):
    Critical = 50
    Error = 40
    Warning = 30
    Info = 20
    Debug = 10
    Trace = 5

    @classmethod
    def try_from_string(cls, s: str) -> Level:
        try:
            return cls.from_string(s)
        except ValueError:
            return Level.Warning

    @classmethod
    def from_string(cls, s: str) -> Level:
        if s.lower() == 'critical':
            return Level.Critical
        elif s.lower() == 'error':
            return Level.Error
        elif s.lower() == 'warning':
            return Level.Warning
        elif s.lower() == 'info':
            return Level.Info
        elif s.lower() == 'debug':
            return Level.Debug
        elif s.lower() == 'trace':
            return Level.Trace
        else:
            raise ValueError(f'Unknown log level {s}')

    @classmethod
    def try_from_verbosity(cls, verbosity: Verbosity) -> Level:
        try:
            return cls.from_verbosity(verbosity)
        except ValueError:
            return Level.Warning

    @classmethod
    def from_verbosity(cls, verbosity: Verbosity) -> Level:
        if verbosity == Verbosity.Error:
            return Level.Error
        elif verbosity == Verbosity.Warning:
            return Level.Warning
        elif verbosity == Verbosity.Info:
            return Level.Info
        elif verbosity == Verbosity.Debug:
            return Level.Debug
        elif verbosity == Verbosity.Trace:
            return Level.Trace
        else:
            raise ValueError(f'Unknown verbosity {verbosity}')


class Verbosity(_Enum):
    Error = 0
    Warning = 1
    Info = 2
    Debug = 3
    Trace = 4

    @classmethod
    def from_int(cls, i: int) -> Verbosity:
        if i <= 0:
            return Verbosity.Error
        elif i == 1:
            return Verbosity.Warning
        elif i == 2:
            return Verbosity.Info
        elif i == 3:
            return Verbosity.Debug
        else:
            return Verbosity.Trace
