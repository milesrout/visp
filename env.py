class Env:
    def __init__(self, bindings=None):
        if bindings is None:
            self.bindings = {}
        else:
            self.bindings = bindings
    def lookup(self, name):
        return self.bindings[name]

    def __add__(self, other):
        new_bindings = {}
        for k, v in other.bindings.items():
            new_bindings[k] = v
        for k, v in self.bindings.items():
            new_bindings[k] = v
        return Env(new_bindings)

    def __radd__(self, other):
        return self + other
