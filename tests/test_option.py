from typing import Any

import pytest

from pytoolkit_option.option import Nothing, Option, Some


class TestSome:
    def test_is_some(self):
        some = Some(42)
        assert some.is_some() is True

    def test_is_none(self):
        some = Some(42)
        assert some.is_none() is False

    def test_unwrap(self):
        some = Some(42)
        assert some.unwrap() == 42

    def test_unwrap_or(self):
        some = Some(42)
        assert some.unwrap_or(0) == 42

    def test_map(self):
        some = Some(42)
        result = some.map(lambda x: x * 2)
        assert isinstance(result, Some)
        assert result.unwrap() == 84

    def test_and_then(self):
        some = Some(42)
        result = some.and_then(lambda x: Some(x * 2))
        assert isinstance(result, Some)
        assert result.unwrap() == 84

    def test_and_then_to_nothing(self):
        some = Some(42)
        result = some.and_then(lambda x: Nothing[int]())
        assert isinstance(result, Nothing)

    def test_match(self):
        some = Some(42)
        result = some.match(some=lambda x: x * 2, nothing=lambda: 0)
        assert result == 84


class TestNothing:
    def test_is_some(self):
        nothing = Nothing[Any]()
        assert nothing.is_some() is False

    def test_is_none(self):
        nothing = Nothing[Any]()
        assert nothing.is_none() is True

    def test_unwrap_raises(self):
        nothing = Nothing[Any]()
        with pytest.raises(ValueError, match="Called unwrap on None"):
            nothing.unwrap()

    def test_unwrap_or(self):
        nothing = Nothing[int]()
        assert nothing.unwrap_or(42) == 42

    def test_map(self):
        nothing = Nothing[int]()
        result = nothing.map(lambda x: x * 2)
        assert isinstance(result, Nothing)

    def test_and_then(self):
        nothing = Nothing[int]()
        result = nothing.and_then(lambda x: Some(x * 2))
        assert isinstance(result, Nothing)

    def test_match(self):
        nothing = Nothing[int]()
        result = nothing.match(some=lambda x: x * 2, nothing=lambda: 42)
        assert result == 42

    def test_new_instance_behavior(self):
        nothing1 = Nothing[Any]()
        nothing2 = Nothing[Any]()
        assert nothing1 is not nothing2
        assert nothing1 != nothing2


class TestOptionGeneric:
    def test_some_with_string(self):
        some = Some("hello")
        assert some.unwrap() == "hello"
        result = some.map(lambda x: x.upper())
        assert result.unwrap() == "HELLO"

    def test_some_with_list(self):
        some = Some([1, 2, 3])
        assert some.unwrap() == [1, 2, 3]
        result = some.map(lambda x: len(x))
        assert result.unwrap() == 3

    def test_chaining_operations(self):
        some = Some(10)
        result = (
            some.map(lambda x: x * 2)
            .and_then(lambda x: Some(x + 5))
            .map(lambda x: str(x))
        )
        assert result.unwrap() == "25"

    def test_chaining_with_nothing(self):
        some = Some(10)
        result = (
            some.map(lambda x: x * 2)
            .and_then(lambda x: Nothing[int]())
            .map(lambda x: str(x))
        )
        assert isinstance(result, Nothing)


class TestOptionPolymorphism:
    def test_option_interface(self):
        options: list[Option[int]] = [Some(42), Nothing()]

        for option in options:
            assert isinstance(option.is_some(), bool)
            assert isinstance(option.is_none(), bool)
            assert option.unwrap_or(0) >= 0

    def test_option_map_polymorphism(self):
        options: list[Option[int]] = [Some(42), Nothing()]

        results = [opt.map(lambda x: x * 2) for opt in options]

        assert isinstance(results[0], Some)
        assert results[0].unwrap() == 84
        assert isinstance(results[1], Nothing)

    def test_option_match_polymorphism(self):
        options: list[Option[int]] = [Some(42), Nothing()]

        results = [
            opt.match(some=lambda x: f"Value: {x}", nothing=lambda: "No value")
            for opt in options
        ]

        assert results[0] == "Value: 42"
        assert results[1] == "No value"
