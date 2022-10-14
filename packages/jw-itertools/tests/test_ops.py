# internal
from jw_types import null
from jw_itertools.ops import (
    Op,
    Map,
    Filter,
    Keep,
    Ops,
    _T,
)


class Identity(Op[_T]):

    def apply(self, value: _T) -> _T:
        return value


identity = Identity()


def test_map():
    assert Map(lambda x: x + 1).apply(1) == 2


def test_filter__filtered():
    assert Filter(lambda x: x == 1).apply(1) is null


def test_filter__not_filtered():
    assert Filter(lambda x: x == 1).apply(2) == 2


def test_keep__filtered():
    assert Keep(lambda x: x == 2).apply(1) is null


def test_keep__not_filtered():
    assert Keep(lambda x: x == 2).apply(2) == 2


def test_ops__op_add_op():
    assert (identity + identity)._ops == [identity, identity]


def test_ops__op_add_ops():
    assert (identity + Ops([identity, identity]))._ops == [identity, identity, identity]


def test_ops__ops_add_op():
    assert (Ops([identity, identity]) + identity)._ops == [identity, identity, identity]


def test_ops__ops_add_ops():
    assert (Ops([identity, identity]) + Ops([identity, identity]))._ops == [identity, identity, identity, identity]


def test_ops__of_empty():
    assert Ops.of()._ops == []


def test_ops__of_single():
    assert Ops.of(identity)._ops == [identity]


def test_ops__of_multiple():
    assert Ops.of(identity, identity)._ops == [identity, identity]


def test_ops__apply__maps():
    m = Map(lambda x: x + 1)
    assert Ops.of(m, m).apply(0) == 2


def test_ops__apply__filter():
    assert Ops.of(Filter(lambda x: x == 1)).apply(1) is null


def test_ops__apply__map_filtered_map():
    ops = Ops.of(
        Map(lambda x: x + 1),
        Filter(lambda x: True),
        Map(lambda x: x + 1),
    )
    assert ops.apply(1) is null
