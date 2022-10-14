# std
from __future__ import annotations
from abc import abstractmethod
import itertools
from typing import Dict, List, Optional as Opt, Union

# external
from jw_datatools.persisted_data import PersistedData, PersistedDataMixin

# types
DependencyDef = Union[str, Dict[str, str]]
DependenciesDef = Dict[str, DependencyDef]


class BuildSystemABC(PersistedDataMixin):

    def __init__(self, build_system_data: PersistedData):
        self.persisted_data: PersistedData = build_system_data

    @abstractmethod
    def get_package_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_version(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_version(self, version: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_group_names(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_group(self, group_name: Opt[str] = None) -> GroupABC:
        raise NotImplementedError

    def get_groups(self) -> List[GroupABC]:
        return [self.get_group(name) for name in self.get_group_names()]

    def get_dependency(self, dependency_name: str, group_name: Opt[str] = None) -> DependencyABC:
        return self.get_group(group_name).get_dependency(dependency_name)

    def get_dependencies(self, group_name: Opt[str] = None) -> List[DependencyABC]:
        return self.get_group(group_name).get_dependencies()

    def get_all_dependencies(self) -> List[DependencyABC]:
        return list(itertools.chain(
            self.get_dependencies(),
            itertools.chain(*(self.get_dependencies(g) for g in self.get_group_names())),
        ))

    @classmethod
    @abstractmethod
    def system_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def build_backend(cls) -> str:
        raise NotImplementedError


class GroupABC(PersistedDataMixin):

    def __init__(
            self,
            name: Opt[str],
            group_data: PersistedData,
    ):
        self.name = name
        self.persisted_data = group_data

    @abstractmethod
    def get_dependency_names(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_dependency(self, dependency_name: str) -> DependencyABC:
        raise NotImplementedError

    def get_dependencies(self) -> List[DependencyABC]:
        return [self.get_dependency(name) for name in self.get_dependency_names()]


class DependencyABC(PersistedDataMixin):

    def __init__(
            self,
            package_name: str,
            group_name: Opt[str],
            dependency_data: PersistedData,
    ):
        self.name = package_name
        self.group_name = group_name
        self.persisted_data = dependency_data

    def __repr__(self) -> str:
        c = 'develop' if self.is_develop() else self.get_constraint()
        g = '' if self.group_name is None else f' ({self.group_name})'
        return f'{self.name} @ {c}{g}'

    @abstractmethod
    def is_develop(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_constraint(self) -> Opt[str]:
        raise NotImplementedError

    @abstractmethod
    def set_constraint(self, constraint: str):
        raise NotImplementedError

    @abstractmethod
    def develop(self, path: str):
        raise NotImplementedError
