from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Iterable, Union
__all__ = ['Filter', 'Never', 'Always', 'Condition', 'FilterOrBool']

class Filter(metaclass=ABCMeta):
    """
    Base class for any filter to activate/deactivate a feature, depending on a
    condition.

    The return value of ``__call__`` will tell if the feature should be active.
    """

    def __init__(self) -> None:
        self._and_cache: dict[Filter, Filter] = {}
        self._or_cache: dict[Filter, Filter] = {}
        self._invert_result: Filter | None = None

    @abstractmethod
    def __call__(self) -> bool:
        """
        The actual call to evaluate the filter.
        """
        return True

    def __and__(self, other: Filter) -> Filter:
        """
        Chaining of filters using the & operator.
        """
        assert isinstance(other, Filter), 'Expecting filter, got %r' % other
        if isinstance(other, Always):
            return self
        if isinstance(other, Never):
            return other
        if other in self._and_cache:
            return self._and_cache[other]
        result = _AndList.create([self, other])
        self._and_cache[other] = result
        return result

    def __or__(self, other: Filter) -> Filter:
        """
        Chaining of filters using the | operator.
        """
        assert isinstance(other, Filter), 'Expecting filter, got %r' % other
        if isinstance(other, Always):
            return other
        if isinstance(other, Never):
            return self
        if other in self._or_cache:
            return self._or_cache[other]
        result = _OrList.create([self, other])
        self._or_cache[other] = result
        return result

    def __invert__(self) -> Filter:
        """
        Inverting of filters using the ~ operator.
        """
        if self._invert_result is None:
            self._invert_result = _Invert(self)
        return self._invert_result

    def __bool__(self) -> None:
        """
        By purpose, we don't allow bool(...) operations directly on a filter,
        because the meaning is ambiguous.

        Executing a filter has to be done always by calling it. Providing
        defaults for `None` values should be done through an `is None` check
        instead of for instance ``filter1 or Always()``.
        """
        raise ValueError('The truth value of a Filter is ambiguous. Instead, call it as a function.')

class _AndList(Filter):
    """
    Result of &-operation between several filters.
    """

    def __init__(self, filters: list[Filter]) -> None:
        super().__init__()
        self.filters = filters

    @classmethod
    def create(cls, filters: Iterable[Filter]) -> Filter:
        """
        Create a new filter by applying an `&` operator between them.

        If there's only one unique filter in the given iterable, it will return
        that one filter instead of an `_AndList`.
        """
        unique_filters = list(set(filters))
        if len(unique_filters) == 0:
            return Always()
        elif len(unique_filters) == 1:
            return unique_filters[0]
        else:
            return cls(unique_filters)

    def __call__(self) -> bool:
        return all((f() for f in self.filters))

    def __repr__(self) -> str:
        return '&'.join((repr(f) for f in self.filters))

class _OrList(Filter):
    """
    Result of |-operation between several filters.
    """

    def __init__(self, filters: list[Filter]) -> None:
        super().__init__()
        self.filters = filters

    @classmethod
    def create(cls, filters: Iterable[Filter]) -> Filter:
        """
        Create a new filter by applying an `|` operator between them.

        If there's only one unique filter in the given iterable, it will return
        that one filter instead of an `_OrList`.
        """
        unique_filters = list(set(filters))
        if len(unique_filters) == 0:
            return Never()
        elif len(unique_filters) == 1:
            return unique_filters[0]
        else:
            return cls(unique_filters)

    def __call__(self) -> bool:
        return any((f() for f in self.filters))

    def __repr__(self) -> str:
        return '|'.join((repr(f) for f in self.filters))

class _Invert(Filter):
    """
    Negation of another filter.
    """

    def __init__(self, filter: Filter) -> None:
        super().__init__()
        self.filter = filter

    def __call__(self) -> bool:
        return not self.filter()

    def __repr__(self) -> str:
        return '~%r' % self.filter

class Always(Filter):
    """
    Always enable feature.
    """

    def __call__(self) -> bool:
        return True

    def __or__(self, other: Filter) -> Filter:
        return self

    def __invert__(self) -> Never:
        return Never()

class Never(Filter):
    """
    Never enable feature.
    """

    def __call__(self) -> bool:
        return False

    def __and__(self, other: Filter) -> Filter:
        return self

    def __invert__(self) -> Always:
        return Always()

class Condition:
    """
    Turn any callable into a Filter. The callable is supposed to not take any
    arguments.

    This can be used as a decorator::

        @Condition
        def feature_is_active():  # `feature_is_active` becomes a Filter.
            return True

    :param func: Callable which takes no inputs and returns a boolean.
    """

    def __init__(self, func: Callable[[], bool]) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Filter:
        """Create a new Filter instance from this callable."""
        if args or kwargs:
            raise ValueError("Condition does not accept any arguments")

        class _Condition(Filter):
            def __init__(self2) -> None:
                super().__init__()
                self2.func = self.func

            def __call__(self2) -> bool:
                return self2.func()

            def __repr__(self2) -> str:
                return 'Condition(%r)' % self2.func

        return _Condition()
FilterOrBool = Union[Filter, bool]