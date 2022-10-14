# std
from __future__ import annotations
from typing import List, Optional as Opt

# internal
from jw_datatools.persisted_data import PersistedData

from tier.internal.build_systems.abstract_build_system import (
    BuildSystemABC,
    GroupABC,
    DependencyABC,
)
from tier.internal.errors import TierException
from tier.internal.versioning.constraint import Constraint


class Poetry(BuildSystemABC):

    def get_package_name(self) -> str:
        return self.get('name')

    def get_version(self) -> str:
        return self.get('version')

    def set_version(self, version: str):
        self.set('version', version)

    def get_group_names(self) -> List[str]:
        return list(self.get('group', {}).keys())

    def get_group(self, group_name: Opt[str] = None) -> GroupABC:
        keys = ['dependencies'] if group_name is None else ['group', group_name]
        return PoetryGroup(group_name, self.view(keys))

    @classmethod
    def system_name(cls) -> str:
        return 'poetry'

    @classmethod
    def build_backend(cls) -> str:
        return 'poetry.core.masonry.api'


class PoetryGroup(GroupABC):

    def get_dependency_names(self) -> List[str]:
        return list(self.get().keys())

    def get_dependency(self, dependency_name: str) -> DependencyABC:
        return PoetryDependency(dependency_name, self.name, self.view(dependency_name))


class PoetryDependency(DependencyABC):

    def exists(self) -> bool:
        return self.get() is not None

    def is_develop(self) -> bool:
        data = self.get()
        return self.exists() and isinstance(data, dict) and data.get('develop', False)

    def get_constraint(self) -> Opt[str]:
        data = self.get()
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            return data.get('version')
        else:
            return None

    def set_constraint(self, constraint: str):
        self.undevelop()
        data = self.get()
        if isinstance(data, str) or (isinstance(data, dict) and len(data) == 0):
            self.set(value=constraint)
        else:
            self.set('version', constraint)

    def develop(self, path: str):
        self.unversion()
        if isinstance(self.get(), str):
            self.set(value={
                'develop': True,
                'path': path,
            })
        else:
            self.set('develop', True)
            self.set('path', path)

    def unversion(self):
        if isinstance(self.get(), str):
            self.set(value={})
        else:
            self.pop('version')

    def undevelop(self):
        if self.is_develop():
            self.pop('develop')
            self.pop('path')

    def _get_constraint_view(self) -> Opt[PersistedData]:
        data = self.get()
        if isinstance(data, str):
            return self.view()
        elif isinstance(data, dict) and 'version' in data:
            return self.view('version')
        else:
            return None
