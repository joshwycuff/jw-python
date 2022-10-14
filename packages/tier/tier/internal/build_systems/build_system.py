# std
from __future__ import annotations

# external
from jw_datatools.persisted_data import PersistedData

# internal
from tier.internal.errors import TierException
from tier.internal.build_systems.abstract_build_system import BuildSystemABC


def get_build_system(project_data: PersistedData) -> BuildSystemABC:
    from tier.internal.build_systems.poetry import Poetry
    project_data = project_data.base()
    build_backend = project_data.get('build-system.build-backend')
    if build_backend == Poetry.build_backend():
        return Poetry(project_data.view('tool.poetry'))
    else:
        raise TierException('Could not determine build system')
