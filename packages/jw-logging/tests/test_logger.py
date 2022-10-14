# std
import logging
import os
from unittest import mock

# internal
from jw_logging import Logger


@mock.patch.dict(os.environ, {'LOG_LEVEL': ''})
def test_create_logger_default():
    assert Logger.create('test')._logger.level == logging.WARNING


@mock.patch.dict(os.environ, {'LOG_LEVEL': 'debug'})
def test_create_logger_with_environment_variable():
    assert Logger.create('test')._logger.level == logging.DEBUG


@mock.patch.dict(os.environ, {'LOG_LEVEL': ''})
def test_create_logger_with_level():
    assert Logger.create('test', 'trace')._logger.level == 5
