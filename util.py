import functools, inspect, sys

def last(iterable):
    for x in iterable:
        pass
    return x

def constructor(__init__):
    @functools.wraps(__init__)
    def new_init(self, *args, **kwds):
        bound_args = inspect.signature(__init__).bind(self, *args, **kwds)
        if sys.version_info >= (3,5): # pragma: no cover
            bound_args.apply_defaults()
        for k, v in bound_args.arguments.items():
            setattr(self, k, v)
        __init__(self, *args, **kwds)
    return new_init

def accumulate(accum_type):
    def outer_wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kwds):
            return accum_type(f(*args, **kwds))
        return inner_wrapper
    return outer_wrapper
