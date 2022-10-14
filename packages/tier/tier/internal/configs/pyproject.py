# std
from __future__ import annotations
import os
from typing import List, Optional as Opt, TYPE_CHECKING

# external
from jw_datatools.persisted_data import PersistedData, PersistedDataMixin

# internal
from tier.internal.build_systems import build_system
from tier.internal.types import Data

if TYPE_CHECKING:
    from tier.internal.build_systems.abstract_build_system import BuildSystemABC


class PyProject(PersistedDataMixin):

    FILENAME = 'pyproject.toml'

    def __init__(self, dirpath: Opt[str] = None, data: Data = None):
        dirpath = dirpath or os.getcwd()
        filepath = os.path.join(dirpath, PyProject.FILENAME)

        self.dirpath = dirpath
        self.filepath = filepath
        self.persisted_data = PersistedData.read_or_new(
            filepath=filepath,
            data=data,
            auto_write=True,
        )

    def get_build_system(self) -> 'BuildSystemABC':
        return build_system.get_build_system(self.persisted_data)

    def get_tool(self, tool_name: str) -> PersistedData:
        return self.view(['tool', tool_name])

    def get_tier_config(self) -> TierConfig:
        return TierConfig(self.get_tool('tier'))

    @classmethod
    def find_recursively(cls, dirpath: Opt[str] = None) -> List[PyProject]:
        dirpath = dirpath or os.getcwd()
        result = []
        for dirpath, dirnames, filenames in os.walk(dirpath):
            if cls.FILENAME in filenames:
                result.append(PyProject(dirpath))
        return result


class TierConfig(PersistedDataMixin):

    def __init__(self, tier_config_data: PersistedData):
        self.persisted_data = tier_config_data

    def get_commit_id(self) -> Opt[str]:
        return self.get('commit-id')

    def set_commit_id(self, value: str):
        return self.set('commit-id', value)

    def get_constraint_strategy(self) -> str:
        return self.get('constraint-strategy', 'minor')

    def set_constraint_strategy(self, value: str):
        return self.get('constraint-strategy', value)
