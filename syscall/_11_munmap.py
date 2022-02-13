import ctypes

from .common import libc, raise_on

__all__ = ["munmap"]

libc.munmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
libc.munmap.restype = ctypes.c_int


@raise_on(lambda rv: rv == -1)
def munmap(addr: int, size: int) -> int:
    """
    int munmap(void *addr, size_t length);
    """
    return libc.munmap(addr, size)


munmap.no = 11
