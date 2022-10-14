# external
import pytest

# internal
from jw_itertools.errors import (
    NoPreviousValueException,
    NoCurrentValueException,
    NoNextValueException, PowerIteratorException,
)
from jw_itertools.power_iterator import PowerIterator


def test__has_previous():
    pi = PowerIterator([])
    assert not pi.has_previous


def test__has_value():
    pi = PowerIterator([])
    assert not pi.has_value


def test__has_next():
    pi = PowerIterator([])
    assert not pi.has_next


def test_iter__empty__has_previous():
    pi = PowerIterator([]).__iter__()
    assert not pi.has_previous


def test_iter__empty__has_value():
    pi = PowerIterator([]).__iter__()
    assert not pi.has_value


def test_iter__empty__has_next():
    pi = PowerIterator([]).__iter__()
    assert not pi.has_next


def test_iter__not_empty__has_previous():
    pi = PowerIterator([1]).__iter__()
    assert not pi.has_previous


def test_iter__not_empty__has_value():
    pi = PowerIterator([1]).__iter__()
    assert not pi.has_value


def test_iter__not_empty__has_next():
    pi = PowerIterator([1]).__iter__()
    assert pi.has_next


def test_next__empty__raises():
    pi = PowerIterator([]).__iter__()
    with pytest.raises(StopIteration):
        next(pi)


def test_next__value():
    pi = PowerIterator([1]).__iter__()
    _, value = next(pi)
    assert value == 1


def test_collect_list():
    assert PowerIterator([1, 2]).collect_list() == [1, 2]


def test_collect_dict():
    assert PowerIterator([('x', 1), ('y', 2)]).collect_dict() == {'x': 1, 'y': 2}


def test_peek_previous():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    next(pi)
    assert pi.p == 1


def test_peek_previous_default():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    assert pi.peek_previous(4) == 4


def test_get_value():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    next(pi)
    assert pi.v == 2


def test_peek_next():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    next(pi)
    assert pi.n == 3


def test_peek_next_default():
    pi = PowerIterator([1]).__iter__()
    next(pi)
    assert pi.peek_next(2) == 2


def test_no_previous_value_exception():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    with pytest.raises(NoPreviousValueException):
        _ = pi.peek_previous()


def test_no_current_value_exception():
    pi = PowerIterator([1, 2, 3]).__iter__()
    with pytest.raises(NoCurrentValueException):
        _ = pi.get_value()


def test_no_next_value_exception():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    next(pi)
    next(pi)
    with pytest.raises(NoNextValueException):
        _ = pi.peek_next()


def test_map():
    pi = PowerIterator([1, 2, 3]).map(lambda x: x + 1)
    assert pi.collect_list() == [2, 3, 4]


def test_filter():
    pi = PowerIterator([1, 2, 3]).filter(lambda x: x == 2)
    assert pi.collect_list() == [1, 3]


def test_keep():
    pi = PowerIterator([1, 2, 3]).keep(lambda x: x == 2)
    assert pi.collect_list() == [2]


def test_i_alias():
    pi = PowerIterator([1]).__iter__()
    _, _ = next(pi)
    assert pi.i == 0


def test_index_alias():
    pi = PowerIterator([1]).__iter__()
    _, _ = next(pi)
    assert pi.index == 0


def test_get_index_raises():
    with pytest.raises(PowerIteratorException):
        _ = PowerIterator([]).get_index()


def test_has_started():
    pi = PowerIterator([1]).__iter__()
    assert pi.has_started


def test_has_not_started():
    pi = PowerIterator([1])
    assert not pi.has_started


def test_has_ended():
    pi = PowerIterator([1]).__iter__()
    next(pi)
    try:
        next(pi)
    except StopIteration:
        pass
    assert pi.has_ended


def test_has_not_ended():
    pi = PowerIterator([1]).__iter__()
    next(pi)
    assert not pi.has_ended


def test_is_first():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    assert pi.is_first


def test_is_not_first():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    next(pi)
    assert not pi.is_first


def test_is_middle():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    next(pi)
    assert pi.is_middle


def test_is_not_middle():
    pi = PowerIterator([1, 2, 3]).__iter__()
    next(pi)
    assert not pi.is_middle
