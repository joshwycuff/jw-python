# std

# internal
from tier.internal.logging import log
from tier.internal.configs.pyproject import PyProject
from tier.internal.tier import Tier


def config(
        recursive: bool,
):
    log.debug('tier config')

    log.debug(f'{recursive = }')

    if recursive:
        projects = PyProject.find_recursively()
    else:
        project = PyProject.from_dirpath(auto_write=True)
