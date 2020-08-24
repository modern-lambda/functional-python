from typing import Callable, Generic, TypeVar, Union

S = TypeVar('S')
T = TypeVar('T')

class Monad(Generic[T]):
    def __init__(self, value, monoid):
        self.value = value
        self.monoid = monoid

    @classmethod
    def apply(cls, function):
        class _Application(cls):
            amap = cls.amap
            bind = cls.bind
            insert = cls.insert
            map = cls.map
            @staticmethod
            def to_arguments(*args):
                results = cls.insert(function)
                for arg in args:
                    results = result.amap(arg)
                return cls(result.value, result.monoid)
        return _Application(None, None)
    
    @classmethod
    def insert(cls, value: T) -> 'Monad[T]':
        raise NotImplementedError

    def amap(self: 'Monad[Callable[[S], T]]', monad_value: 'Monad[S]') -> 'Monad[T]':
        return monad_value.map(self.value)

    def bind(self: 'Monad[S]', kleisli_function: Callable[[S], 'Monad[T]']) -> 'Monad[T]':
        raise NotImplementedError

    def map(self: 'Monad[S]', function: Callable[[S], T]) -> 'Monad[T]':
        raise NotImplementedError("'fmap' not defined.")

    def then(
        self: 'Monad[S]', function: Union[Callable[[S], T], Callable[[S], 'Monad[T]']]
    ) -> 'Monad[T]':
        try:
            result = self.bind(function)
            if isinstance(result, Monad):
                return result
            else:
                return self.map(function)
        except AttributeError:
            return self.map(function)