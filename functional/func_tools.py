import inspect
import operator
from functools import reduce, partial

def identity(x):
    return x

def apply(*func_and_args, **kwargs):
    if not func_and_args:
        raise TypeError('function argument is required.')
    func, args = func_and_args[0], func_and_args[1:]
    return func(*args, **kwargs)

def thread_first(val, *forms):
    def evalform_front(val, form):
        if callable(form):
            return form(val)
        if isinstance(form, tuple):
            func, args = form[0], form[1:]
            args = (val,) + args
            return func(*args)
    return reduce(evalform_back, forms, val)

class curry(object):
    def __init__(self, *args, **kwargs):
        if not args:
            raise TypeError('__init__() takes at least 2 arguments (1 given)')
        func, args = args[0], args[1:]
        if not callable(func):
            raise TypeError("Input must be callable")

        if (
            hasattr(func, 'func')
            and hasattr(func, 'args')
            and hasattr(func, 'keywords')
            and isinstance(func.args, tuple)
        ):
            _kwargs = {}
            if func.keywords:
                _kwargs.update(func.keywords)
            _kwargs.update(kwargs)
            kwargs = _kwargs
            args = func.args + args
            func = func.func
        
        if kwargs:
            self._partial = partial(func, *args, **kwargs)
        else:
            self._partial = partial(func, *args)



