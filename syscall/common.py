import errno
import ctypes
import functools
import ctypes.util

libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)


class Structure(ctypes.Structure):
    def byref(self):
        return ctypes.byref(self)

    def sizeof(self):
        return ctypes.sizeof(self)


def raise_on(cond):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kws):
            rv = func(*args, **kws)
            if cond(rv):
                raise OSError(errno.errorcode[ctypes.get_errno()])
            return rv
        return wrapper
    return inner
