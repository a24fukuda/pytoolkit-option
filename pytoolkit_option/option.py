from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Option(ABC, Generic[T]):
    @abstractmethod
    def is_some(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_none(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def unwrap(self) -> T:
        raise NotImplementedError()

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Option[U]:
        raise NotImplementedError()

    @abstractmethod
    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        raise NotImplementedError()

    @abstractmethod
    def match(self, some: Callable[[T], U], none: Callable[[], U]) -> U:
        raise NotImplementedError()


@dataclass(frozen=True)
class Some(Option[T]):
    _value: T

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def map(self, f: Callable[[T], U]) -> Option[U]:
        return Some(f(self._value))

    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        return f(self._value)

    def match(self, some: Callable[[T], U], none: Callable[[], U]) -> U:
        return some(self._value)


class Nothing(Option[T]):
    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True

    def unwrap(self) -> T:
        raise ValueError("Called unwrap on None")

    def unwrap_or(self, default: T) -> T:
        return default

    def map(self, f: Callable[[T], U]) -> Option[U]:
        return Nothing[U]()

    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        return Nothing[U]()

    def match(self, some: Callable[[T], U], none: Callable[[], U]) -> U:
        return none()
