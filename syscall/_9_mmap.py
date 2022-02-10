import ctypes

from .common import libc, raise_on

__all__ = ["PROT_READ", "PROT_WRITE", "MAP_PRIVATE", "MAP_ANONYMOUS", "mmap"]

PROT_READ = 0x1
PROT_WRITE = 0x2
MAP_PRIVATE = 0x02
MAP_ANONYMOUS = 0x20

libc.mmap.argtypes = [
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_long,
]
libc.mmap.restype = ctypes.c_void_p


@raise_on(lambda rv: rv == -1)
def mmap(
    addr: int, length: int, prot: int, flags: int, fd: int, offset: int
) -> int:
    """
    void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset); # noqa
    """
    return libc.mmap(addr, length, prot, flags, fd, offset)


mmap.no = 9

if __name__ == "__main__":
    import os
    import sys

    filename = sys.argv[1]
    offset = int(sys.argv[2])
    length = int(sys.argv[3])

    page_size = os.sysconf(os.sysconf_names["SC_PAGE_SIZE"])
    pa_offset = offset & ~(page_size - 1)

    with open(filename) as f:
        sb = os.fstat(f.fileno())
        if offset + length > sb.st_size:
            length = sb.st_size - offset

        addr = mmap(
            0,
            length + offset - pa_offset,
            PROT_READ,
            MAP_PRIVATE,
            f.fileno(),
            pa_offset,
        )
        print(ctypes.cast(addr, ctypes.c_char_p).value)
