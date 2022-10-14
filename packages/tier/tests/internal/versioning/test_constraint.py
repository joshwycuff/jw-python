# internal
from tier.internal.versioning.version import Version
from tier.internal.versioning.constraint import Constraint


def test_exact():
    assert str(Constraint.exact(Version(1, 2, 3))) == '1.2.3'


def test_minor():
    assert str(Constraint.minor(Version(1, 2, 3))) == '>=1.2.3,<1.3'


def test_major():
    assert str(Constraint.major(Version(1, 2, 3))) == '>=1.2,<2'
