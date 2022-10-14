# std
from __future__ import annotations as _annotations
import json as _json
from logging import (
    getLogger as _getLogger,
    Formatter as _Formatter,
    Logger as _Logger,
    StreamHandler as _StreamHandler,
)
from os import environ as _environ
import sys as _sys
from typing import Optional as _Opt, Union as _Union

# internal
from jw_logging.level import Level as _Level, Verbosity as _Verbosity


class Logger:
    DEFAULT_FORMAT = '%(asctime)s (%(name)s) [%(levelname)s] %(message)s'
    DEFAULT_LEVEL = 'WARNING'

    def __init__(self, name: str):
        self._name: str = name
        self._logger: _Logger = _getLogger(name)

    @property
    def name(self) -> str:
        return self._name

    def log(self, msg: str, level: int):
        self._logger.log(level, msg)

    def critical(self, msg: str):
        self._logger.critical(msg)

    def error(self, msg: str):
        self._logger.error(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def info(self, msg: str):
        self._logger.info(msg)

    def debug(self, msg: str):
        self._logger.debug(msg)

    def trace(self, msg: str):
        self._logger.log(5, msg)

    def jcritical(self, msg: object, pretty: bool = False, safe: bool = True, **kwargs):
        if pretty:
            kwargs['indent'] = 2
        if safe:
            kwargs['default'] = str
        self.critical(_json.dumps(msg, **kwargs))

    def jerror(self, msg: object, pretty: bool = False, safe: bool = True, **kwargs):
        if pretty:
            kwargs['indent'] = 2
        if safe:
            kwargs['default'] = str
        self.error(_json.dumps(msg, **kwargs))

    def jwarning(self, msg: object, pretty: bool = False, safe: bool = True, **kwargs):
        if pretty:
            kwargs['indent'] = 2
        if safe:
            kwargs['default'] = str
        self.warning(_json.dumps(msg, **kwargs))

    def jinfo(self, msg: object, pretty: bool = False, safe: bool = True, **kwargs):
        if pretty:
            kwargs['indent'] = 2
        if safe:
            kwargs['default'] = str
        self.info(_json.dumps(msg, **kwargs))

    def jdebug(self, msg: object, pretty: bool = False, safe: bool = True, **kwargs):
        if pretty:
            kwargs['indent'] = 2
        if safe:
            kwargs['default'] = str
        self.debug(_json.dumps(msg, **kwargs))

    def jtrace(self, msg: object, pretty: bool = False, safe: bool = True, **kwargs):
        if pretty:
            kwargs['indent'] = 2
        if safe:
            kwargs['default'] = str
        self.trace(_json.dumps(msg, **kwargs))

    @classmethod
    def create(
            cls,
            name: str,
            level: _Opt[_Union[int, str]] = None,
            verbosity: _Opt[int] = None,
            fmt: _Opt[str] = None,
            propagate: bool = False,
    ) -> Logger:
        logger = _getLogger(name)
        logger.propagate = propagate

        if isinstance(level, str):
            level = level.upper()

        verbosity_as_level = None
        if verbosity is not None:
            verbosity_as_level = _Level.from_verbosity(_Verbosity.from_int(verbosity)).value

        environment_log_level = _Level.try_from_string(_environ.get('LOG_LEVEL', '').upper()).value

        level = level or verbosity_as_level or environment_log_level or cls.DEFAULT_LEVEL
        logger.setLevel(level)

        handler = _StreamHandler(_sys.stderr)
        handler.setFormatter(_Formatter(fmt=fmt or cls.DEFAULT_FORMAT))
        logger.addHandler(handler)

        return Logger(name)

    @classmethod
    def get_or_create(
            cls,
            name: str,
            level: _Opt[_Union[int, str]] = None,
            verbosity: _Opt[int] = None,
            fmt: _Opt[str] = None,
            propagate: bool = False,
    ) -> Logger:
        if name in _Logger.manager.loggerDict:
            return _getLogger(name)
        else:
            return cls.create(
                level=level,
                verbosity=verbosity,
                fmt=fmt,
                propagate=propagate,
            )
