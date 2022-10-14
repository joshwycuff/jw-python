# internal
import pytest

from tier.internal.errors import TierVersionError
from tier.internal.versioning.version import Version


def test__constructor__major():
    assert Version(1).major == 1


def test__constructor__minor():
    assert Version(1, 2).minor == 2


def test__constructor__patch():
    assert Version(1, 2, 3).patch == 3


def test__constructor__post():
    assert Version(1, 2, 3, post=4).post == 4


def test__constructor__rc():
    assert Version(1, 2, 3, rc=4).rc == 4


def test__constructor__b():
    assert Version(1, 2, 3, b=4).b == 4


def test__constructor__a():
    assert Version(1, 2, 3, a=4).a == 4


def test__constructor__dev():
    assert Version(1, 2, 3, dev=4).dev == 4


def test__constructor__version_error():
    with pytest.raises(TierVersionError):
        _ = Version(1, 2, 3, a=4, b=5)


def test__validate__success():
    assert Version.validate('1.2.3')


def test__validate__require_minor_patch():
    assert not Version.validate('1')


def test__validate__disallow_dev_alpha():
    assert not Version.validate('1.2.3.dev4a5')


def test__validate__disallow_alpha_beta():
    assert not Version.validate('1.2.3a4b5')


def test__validate__disallow_beta_rc():
    assert not Version.validate('1.2.3b4rc5')


def test__validate__disallow_rc_post():
    assert not Version.validate('1.2.3rc4.post5')


def test__from_str__major():
    assert Version.from_str('1.2.3').major == 1


def test__from_str__minor():
    assert Version.from_str('1.2.3').minor == 2


def test__from_str__patch():
    assert Version.from_str('1.2.3').patch == 3


def test__from_str__dev():
    assert Version.from_str('1.2.3.dev4').dev == 4


def test__from_str__alpha():
    assert Version.from_str('1.2.3a4').a == 4


def test__from_str__beta():
    assert Version.from_str('1.2.3b4').b == 4


def test__from_str__rc():
    assert Version.from_str('1.2.3rc4').rc == 4


def test__from_str__post():
    assert Version.from_str('1.2.3.post4').post == 4


def test__str():
    assert Version(1, 2, 3).str() == '1.2.3'


def test__repr():
    assert Version(1, 2, 3).repr() == '1.2.3'


def test__str__():
    assert str(Version(1, 2, 3)) == '1.2.3'


def test__repr__():
    assert repr(Version(1, 2, 3)) == '1.2.3'


def test__lt__1():
    assert Version.from_str('1.1.1') < Version.from_str('2.2.2')


def test__lt__2():
    assert Version.from_str('2.1.1') < Version.from_str('2.2.2')


def test__lt__3():
    assert Version.from_str('2.2.1') < Version.from_str('2.2.2')


def test__lt__4():
    assert not (Version.from_str('2.2.2') < Version.from_str('2.2.2'))


def test__lt__dev_dev():
    assert Version.from_str('1.1.1.dev1') < Version.from_str('1.1.1.dev2')


def test__lt__dev_a():
    assert Version.from_str('1.1.1.dev1') < Version.from_str('1.1.1a1')


def test__lt__dev_b():
    assert Version.from_str('1.1.1.dev1') < Version.from_str('1.1.1b1')


def test__lt__dev_rc():
    assert Version.from_str('1.1.1.dev1') < Version.from_str('1.1.1rc1')


def test__lt__dev_none():
    assert Version.from_str('1.1.1.dev1') < Version.from_str('1.1.1')


def test__lt__dev_post():
    assert Version.from_str('1.1.1.dev1') < Version.from_str('1.1.1.post1')


def test__lt__a_dev():
    assert not (Version.from_str('1.1.1a1') < Version.from_str('1.1.1.dev1'))


def test__lt__a_a():
    assert Version.from_str('1.1.1a1') < Version.from_str('1.1.1a2')


def test__lt__a_b():
    assert Version.from_str('1.1.1a1') < Version.from_str('1.1.1b1')


def test__lt__a_rc():
    assert Version.from_str('1.1.1a1') < Version.from_str('1.1.1rc1')


def test__lt__a_none():
    assert Version.from_str('1.1.1a1') < Version.from_str('1.1.1')


def test__lt__a_post():
    assert Version.from_str('1.1.1a1') < Version.from_str('1.1.1.post1')


def test__lt__b_dev():
    assert not (Version.from_str('1.1.1b1') < Version.from_str('1.1.1.dev1'))


def test__lt__b_a():
    assert not (Version.from_str('1.1.1b1') < Version.from_str('1.1.1a1'))


def test__lt__b_b():
    assert Version.from_str('1.1.1b1') < Version.from_str('1.1.1b2')


def test__lt__b_rc():
    assert Version.from_str('1.1.1b1') < Version.from_str('1.1.1rc1')


def test__lt__b_none():
    assert Version.from_str('1.1.1b1') < Version.from_str('1.1.1')


def test__lt__b_post():
    assert Version.from_str('1.1.1b1') < Version.from_str('1.1.1.post1')


def test__lt__rc_dev():
    assert not (Version.from_str('1.1.1rc1') < Version.from_str('1.1.1.dev1'))


def test__lt__rc_a():
    assert not (Version.from_str('1.1.1rc1') < Version.from_str('1.1.1a1'))


def test__lt__rc_b():
    assert not (Version.from_str('1.1.1rc1') < Version.from_str('1.1.1b1'))


def test__lt__rc_rc():
    assert Version.from_str('1.1.1rc1') < Version.from_str('1.1.1rc2')


def test__lt__rc_none():
    assert Version.from_str('1.1.1rc1') < Version.from_str('1.1.1')


def test__lt__rc_post():
    assert Version.from_str('1.1.1rc1') < Version.from_str('1.1.1.post1')


def test__lt__none_dev():
    assert not (Version.from_str('1.1.1') < Version.from_str('1.1.1.dev1'))


def test__lt__none_a():
    assert not (Version.from_str('1.1.1') < Version.from_str('1.1.1a1'))


def test__lt__none_b():
    assert not (Version.from_str('1.1.1') < Version.from_str('1.1.1b1'))


def test__lt__none_rc():
    assert not (Version.from_str('1.1.1') < Version.from_str('1.1.1rc1'))


def test__lt__none_none():
    assert Version.from_str('1.1.1') < Version.from_str('1.1.2')


def test__lt__none_post():
    assert Version.from_str('1.1.1') < Version.from_str('1.1.1.post1')


def test__lt__post_dev():
    assert not (Version.from_str('1.1.1.post1') < Version.from_str('1.1.1.dev1'))


def test__lt__post_a():
    assert not (Version.from_str('1.1.1.post1') < Version.from_str('1.1.1a1'))


def test__lt__post_b():
    assert not (Version.from_str('1.1.1.post1') < Version.from_str('1.1.1b1'))


def test__lt__post_rc():
    assert not (Version.from_str('1.1.1.post1') < Version.from_str('1.1.1rc1'))


def test__lt__post_none():
    assert not (Version.from_str('1.1.1.post1') < Version.from_str('1.1.1'))


def test__lt__post_post():
    assert Version.from_str('1.1.1.post1') < Version.from_str('1.1.1.post2')


def test__bump__major():
    assert Version(1, 2, 3).bump_major() == Version(2)


def test__bump__minor():
    assert Version(1, 2, 3).bump_minor() == Version(1, 3)


def test__bump__patch():
    assert Version(1, 2, 3).bump_patch() == Version(1, 2, 4)


def test__bump__post():
    assert Version(1, 2, 3).bump_post() == Version(1, 2, 3, 0)


def test__bump__rc():
    assert Version(1, 2, 3).bump_rc() == Version(1, 2, 3, rc=0)


def test__bump__b():
    assert Version(1, 2, 3).bump_b() == Version(1, 2, 3, b=0)


def test__bump__a():
    assert Version(1, 2, 3).bump_a() == Version(1, 2, 3, a=0)


def test__bump__dev():
    assert Version(1, 2, 3).bump_dev() == Version(1, 2, 3, dev=0)


def test__dev__bump__dev():
    assert Version(1, 2, 3, dev=0).bump_dev() == Version(1, 2, 3, dev=1)
