# internal
from tier.internal.versioning.bump_type import BumpType


def test_major_add_major_equals_major():
    assert BumpType.MAJOR + BumpType.MAJOR == BumpType.MAJOR


def test_major_add_minor_equals_major():
    assert BumpType.MAJOR + BumpType.MINOR == BumpType.MAJOR


def test_major_add_patch_equals_major():
    assert BumpType.MAJOR + BumpType.PATCH == BumpType.MAJOR


def test_major_add_post_equals_major():
    assert BumpType.MAJOR + BumpType.POST == BumpType.MAJOR


def test_major_add_rc_equals_major_rc():
    assert BumpType.MAJOR + BumpType.RC == BumpType.MAJOR_RC


def test_major_add_major_rc_equals_major_rc():
    assert BumpType.MAJOR + BumpType.MAJOR_RC == BumpType.MAJOR_RC


def test_major_add_b_equals_major_b():
    assert BumpType.MAJOR + BumpType.B == BumpType.MAJOR_B


def test_major_add_a_equals_major_a():
    assert BumpType.MAJOR + BumpType.A == BumpType.MAJOR_A


def test_major_add_dev_equals_major_dev():
    assert BumpType.MAJOR + BumpType.DEV == BumpType.MAJOR_DEV


def test_post_add_rc_equals_post():
    assert BumpType.POST + BumpType.RC == BumpType.POST
