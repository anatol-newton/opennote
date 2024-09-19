from typing import Any


def get_repr(py_object: Any):
    out = f'{py_object.__class__.__name__}('

    first = True

    for var in vars(py_object):
        if first:
            first = False
        else:
            out += ", "
        out += var
        out += "="
        out += vars(py_object)[var].__repr__()

    out += ")"

    return out
