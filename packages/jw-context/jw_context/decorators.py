# std
from contextlib import AbstractContextManager as _AbstractContextManager
from functools import wraps as _wraps

# internal
from jw_context.context_managers import (
    EnvironmentVariables as _EnvironmentVariables,
    InDir as _InDir,
    InTmpDir as _InTmpDir,
)


def context_manager_as_decorator(cls: type(_AbstractContextManager)):
    @_wraps(cls.__init__)
    def context_manager_outer_func(**cm_kwargs):
        def context_manager_decorator(func):
            @_wraps(func)
            def context_manager_wrapper(*args, **kwargs):
                with cls(**cm_kwargs):
                    return func(*args, **kwargs)
            return context_manager_wrapper
        return context_manager_decorator
    return context_manager_outer_func


environment_variables = context_manager_as_decorator(_EnvironmentVariables)
in_dir = context_manager_as_decorator(_InDir)
in_tmp_dir = context_manager_as_decorator(_InTmpDir)
