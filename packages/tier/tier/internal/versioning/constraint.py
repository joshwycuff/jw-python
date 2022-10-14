# std
from __future__ import annotations

# internal
from tier.internal.errors import TierValidationException
from tier.internal.versioning.version import Version


class Constraint:

    def __init__(self, constraint: str = "*"):
        self.constraint = constraint

    def __repr__(self):
        return self.constraint

    def str(self) -> str:
        return self.constraint

    def is_develop(self) -> bool:
        return self.constraint == 'develop'

    @classmethod
    def exact(cls, v: Version) -> Constraint:
        return Constraint(v.str())

    @classmethod
    def minor(cls, v: Version) -> Constraint:
        return Constraint(f'>={v.major}.{v.minor}.{v.patch},<{v.major}.{v.minor+1}')

    @classmethod
    def major(cls, v: Version) -> Constraint:
        return Constraint(f'>={v.major}.{v.minor},<{v.major+1}')

    @classmethod
    def develop(cls) -> Constraint:
        return Constraint('develop')

    @classmethod
    def from_strategy(cls, v: Version, strategy: str = 'major') -> Constraint:
        if strategy.lower() == 'major':
            return Constraint.major(v)
        elif strategy.lower() == 'minor':
            return Constraint.minor(v)
        elif strategy.lower() == 'exact':
            return Constraint.exact(v)
        elif strategy.lower() == 'develop':
            return Constraint.develop()
        else:
            raise TierValidationException(f'Unknown constraint strategy {strategy}')
