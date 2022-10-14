# std
from __future__ import annotations as _annotations
from collections.abc import Iterator as _IteratorABC
from typing import (
    Callable as _Callable,
    Generic as _Generic,
    Iterable as _Iterable,
    Iterator as _Iterator,
    List as _List,
    Optional as _Opt,
    Tuple as _Tuple,
    TypeVar as _TypeVar,
    Union as _Union,
)

# internal
from jw_itertools.errors import (
    no_previous_value_exception as _no_previous_value_exception,
    no_current_value_exception as _no_current_value_exception,
    no_next_value_exception as _no_next_value_exception,
    PowerIteratorException as _PowerIteratorException,
)
from jw_itertools.ops import (
    null,
    Op,
    Map,
    Filter,
    Keep,
    Ops,
)

# types
_T = _TypeVar('_T')
_U = _TypeVar('_U')
_V = _TypeVar('_V')


class PowerIterator(_IteratorABC, _Generic[_T, _U]):

    def __init__(self, iterable: _Iterable, ops: _Opt[Ops] = None):
        self._iterable: _Iterable = iterable
        self._iterator: _Opt[_Iterator] = None
        self._index: _Opt[int] = None
        self._ops: Ops = Ops.empty() if ops is None else ops
        self._previous = _no_previous_value_exception
        self._current = _no_current_value_exception
        self._next = _no_next_value_exception

    def __iter__(self) -> PowerIterator[_T, _U]:
        self._iterator = iter(self._iterable)
        self._index = -1
        self._next = self._try_next()
        return self

    def __next__(self) -> _Tuple[PowerIterator[_T, _U], _U]:
        self._shift()
        if self._current is _no_next_value_exception:
            raise StopIteration
        return self, self.get_value()

    @property
    def p(self) -> _U:
        return self.peek_previous()

    @property
    def v(self) -> _U:
        return self.get_value()

    @property
    def i(self) -> int:
        return self.get_index()

    @property
    def index(self) -> int:
        return self.get_index()

    @property
    def n(self) -> _U:
        return self.peek_next()

    @property
    def has_started(self) -> bool:
        return self._index is not None

    @property
    def has_previous(self) -> bool:
        return self.has_started and self._index > 0

    @property
    def has_value(self) -> bool:
        return not isinstance(self._current, _PowerIteratorException)

    @property
    def has_next(self) -> bool:
        return self._next is not _no_next_value_exception

    @property
    def has_ended(self) -> bool:
        return self.has_started and not self.has_value

    @property
    def is_first(self) -> bool:
        return self.has_started and self._index == 0

    @property
    def is_middle(self) -> bool:
        return self.has_started and self._index > 0 and not self.is_last

    @property
    def is_last(self) -> bool:
        return self.has_started and not self.has_next

    def peek_previous(self, default: _Union[_U, null.type()] = null) -> _U:
        if self.has_previous:
            return self._previous
        elif default is not null:
            return default
        else:
            raise _no_previous_value_exception

    def get_value(self) -> _U:
        if self.has_value:
            return self._current
        else:
            raise _no_current_value_exception

    def get_index(self) -> _U:
        if self._index is None:
            _PowerIteratorException.not_started()
        else:
            return self._index

    def peek_next(self, default: _Union[_U, null.type()] = null) -> _U:
        if self.has_next:
            return self._next
        elif default is not null:
            return default
        else:
            raise _no_next_value_exception

    def map(self, callable: _Callable[[_T], _V]) -> PowerIterator[_T, _V]:
        self._ops += Map(callable)
        return self

    def filter(self, callable: _Callable[[_T], bool]) -> PowerIterator[_T, _V]:
        self._ops += Filter(callable)
        return self

    def keep(self, callable: _Callable[[_T], bool]) -> PowerIterator[_T, _V]:
        self._ops += Keep(callable)
        return self

    def collect_list(self):
        return [value for _, value in self]

    def collect_dict(self):
        return dict(value for _, value in self)

    def _shift(self):
        self._previous, self._current, self._next = self._current, self._next, self._try_next()
        self._index += 1

    def _try_next(self):
        try:
            value = self._ops.apply(next(self._iterator))
            while value is null:
                value = self._ops.apply(next(self._iterator))
            return value
        except StopIteration:
            return _no_next_value_exception
