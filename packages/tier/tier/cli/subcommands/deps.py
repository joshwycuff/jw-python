# std
from typing import List

# external
from jw_itertools.power_iterator import PowerIterator

# internal
from tier.internal.logging import log
from tier.internal.tier import Tier
from tier.internal.configs.pyproject import PyProject
from tier.internal.build_systems.abstract_build_system import (
    BuildSystemABC,
    DependencyABC,
)


def deps():
    log.debug('tier deps')
    tier = Tier()
    projects: List[PyProject] = list(tier.projects())
    print('.')
    for pi1, project in PowerIterator(projects):
        build_system: BuildSystemABC = project.get_build_system()
        package_name = build_system.get_package_name()
        prefix = '└──' if pi1.is_last else '├──'
        print(f'{prefix} {package_name}')
        dependencies: List[DependencyABC] = build_system.get_all_dependencies()
        dependencies = tier.graph.keep_internal_dependencies(dependencies)
        for pi2, dependency in PowerIterator(dependencies):
            prefix1 = ' ' if pi1.is_last else '│'
            prefix2 = '└──' if pi2.is_last else '├──'
            print(f'{prefix1}   {prefix2} {dependency}')
