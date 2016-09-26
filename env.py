"""Environment and assignable value cell implementation for Visp.

Without Cell, (set! k v) would only set a value for the remainder of the
current scope."""

class Cell:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

class BaseEnv:
    # the mutable default value is fine because we don't mutate it
    # never directly use or mutate this default!
    def __init__(self, bindings={}):
        self.bindings = {}
        for k, v in bindings.items():
            if isinstance(v, Cell):
                self.bindings[k] = v
            else:
                self.bindings[k] = Cell(v)

    def add(self, name, value=None):
        """Add a new entry to the environment
        
        If we add a Cell to the environment, just insert it
        into the bindings. If we add something else, wrap it in a
        Cell so that it can be mutated later."""
        if isinstance(value, Cell):
            self.bindings[name] = value
        else:
            self.bindings[name] = Cell(value)

    def lookup(self, name):
        return self.bindings[name].get()

    def set(self, name, value):
        self.bindings[name].set(value)

    def __add__(self, other):
        new_bindings = {}
        for k, v in other.bindings.items():
            new_bindings[k] = v
        for k, v in self.bindings.items():
            new_bindings[k] = v
        return BaseEnv(new_bindings)

    def __radd__(self, other):
        return self + other
