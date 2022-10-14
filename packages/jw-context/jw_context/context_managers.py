# std
from contextlib import (
    AbstractContextManager as _AbstractContextManager,
    ExitStack as _ExitStack,
)
import os as _os
import tempfile as _tempfile
from typing import (
    Dict as _Dict,
    List as _List,
)


class EnvironmentVariables(_AbstractContextManager):

    def __init__(self, **environment_variables: str):
        self.previous_values = {}
        self.environment_variables = environment_variables

    def __enter__(self):
        for key, val in self.environment_variables.items():
            self.previous_values[key] = _os.environ.get(key)
            _os.environ[key] = val

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key in self.environment_variables.keys():
            val = self.previous_values[key]
            if val is None:
                del _os.environ[key]
            else:
                _os.environ[key] = val


class InDir(_AbstractContextManager):

    def __init__(self, dirpath: str):
        self.cwd = None
        self.dirpath = dirpath

    def __enter__(self):
        self.cwd = _os.getcwd()
        _os.chdir(self.dirpath)
        return self.dirpath

    def __exit__(self, exc_type, exc_val, exc_tb):
        _os.chdir(self.cwd)


class InTmpDir(_AbstractContextManager):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.stack = _ExitStack()

    def __enter__(self):
        tmp = _tempfile.TemporaryDirectory(**self.kwargs)
        self.stack.enter_context(tmp)
        self.stack.enter_context(InDir(tmp.name))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stack.__exit__(exc_type, exc_val, exc_tb)


class ContextStack(_AbstractContextManager):

    def __init__(self, *context_managers: _AbstractContextManager):
        self.context_managers: _List[_AbstractContextManager] = list(context_managers)
        self.exit_stack: _ExitStack = _ExitStack()

    def __enter__(self):
        for context_manager in self.context_managers:
            self.exit_stack.enter_context(context_manager)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_stack.__exit__(exc_type, exc_val, exc_tb)
