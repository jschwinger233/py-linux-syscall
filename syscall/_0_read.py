import errno
import ctypes
import typing

from .common import libc

__all__ = ["read"]

libc.read.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t]


def read(fd: int, buf: typing.Any, count: int) -> int:
    """
    ssize_t read(int fd, void *buf, size_t count);
    """
    res = libc.read(fd, ctypes.pointer(buf), count)
    if res < 0:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res


read.syscall_no = 0
