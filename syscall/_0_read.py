import ctypes

from .common import libc, raise_on

__all__ = ["read"]

libc.read.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t]
libc.read.restype = ctypes.c_ssize_t


@raise_on(lambda rv: rv < 0)
def read(fd: int, buf: int, count: int) -> int:
    """
    ssize_t read(int fd, void *buf, size_t count);
    """
    return libc.read(fd, buf, count)


read.no = 0
