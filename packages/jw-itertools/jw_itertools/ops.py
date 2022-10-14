# std
from __future__ import annotations as _annotations
from abc import abstractmethod as _abstractmethod
from typing import (
    Callable as _Callable,
    Generic as _Generic,
    List as _List,
    TypeVar as _TypeVar,
    Union as _Union,
)

# external
from jw_types import null

# types
_T = _TypeVar('_T')
_U = _TypeVar('_U')
_V = _TypeVar('_V')


class Op(_Generic[_T]):

    @_abstractmethod
    def apply(self, value: _T):
        raise NotImplementedError

    def __add__(self, other: _Union[Op, Ops]) -> Ops:
        if isinstance(other, Op):
            return Ops([self, other])
        else:
            return other + self


class Map(Op, _Generic[_T, _U]):

    def __init__(self, mapper: _Callable[[_T], _U]):
        self._mapper = mapper

    def apply(self, value: _T) -> _U:
        if value is null:
            return value
        else:
            return self._mapper(value)


class Filter(Op[_T]):

    def __init__(self, filterer: _Callable[[_T], bool]):
        self._filterer = filterer

    def apply(self, value: _T) -> _Union[_T, null]:
        if self._filterer(value):
            return null
        else:
            return value


class Keep(Op[_T]):

    def __init__(self, keeper: _Callable[[_T], bool]):
        self._keeper = keeper

    def apply(self, value: _T) -> _Union[_T, null]:
        if self._keeper(value):
            return value
        else:
            return null


class Ops(_Generic[_T, _U]):

    def __init__(self, ops: _List[Op]):
        self._ops: _List[Op] = list(ops)

    def __add__(self, other: _Union[Op, Ops]) -> Ops:
        if isinstance(other, Op):
            return Ops(self._ops + [other])
        else:
            return Ops(self._ops + other._ops)

    def apply(self, value: _T) -> _U:
        for op in self._ops:
            value = op.apply(value)
        return value

    @classmethod
    def of(cls, *ops: Op) -> Ops:
        return Ops(list(ops))

    @classmethod
    def empty(cls) -> Ops:
        return _empty


_empty = Ops.of()
