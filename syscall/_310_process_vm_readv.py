import ctypes

from .common import libc, Structure, raise_on

__all__ = ["process_vm_readv"]

libc.process_vm_readv.argtypes = [
    ctypes.c_int,  # pid_t pid
    ctypes.c_void_p,  # const struct iovec *local_iov
    ctypes.c_ulong,  # unsigned long liovcnt
    ctypes.c_void_p,  # const struct iovec *remote_iov
    ctypes.c_ulong,  # unsigned long riovcnt
    ctypes.c_ulong,  # unsigned long flags
]
libc.process_vm_readv.restype = ctypes.c_int

libc.process_vm_readv = raise_on(lambda rv: rv == -1)(libc.process_vm_readv)


def process_vm_readv(pid: int, remote_vecs: [(int, int)]) -> [bytes]:
    n = len(remote_vecs)
    Iovecs = Iovec * n

    remote_iov = Iovecs(
        *[
            Iovec(ctypes.cast(iov_base, ctypes.c_void_p), iov_len)
            for iov_base, iov_len in remote_vecs
        ]
    )

    local_vecs = []
    for _, iov_len in remote_vecs:
        buf = (ctypes.c_byte * iov_len)()
        local_vecs.append((ctypes.byref(buf), iov_len))
    local_iov = Iovecs(
        *[
            Iovec(ctypes.cast(iov_base, ctypes.c_void_p), iov_len)
            for iov_base, iov_len in local_vecs
        ]
    )

    rv = libc.process_vm_readv(
        pid,
        ctypes.byref(local_iov),
        n,
        ctypes.byref(remote_iov),
        n,
        0,
    )

    res = []
    for vec in local_vecs:
        res.append(
            bytes(
                ctypes.cast(
                    vec[0], ctypes.POINTER(ctypes.c_byte * vec[1])
                ).contents
            )
        )

    if rv < sum(iov_len for _, iov_len in remote_vecs):
        s = 0
        for idx, (_, iov_len) in enumerate(remote_vecs):
            s += iov_len
            if s >= rv:
                break
        tails = process_vm_readv(pid, remote_vecs[idx:])
        del res[idx:]
        res.extend(tails)
    return res


process_vm_readv.no = 310


class Iovec(Structure):
    """
    struct iovec {
        void  *iov_base;    /* Starting address */
        size_t iov_len;     /* Number of bytes to transfer */
    };
    """

    _fields_ = (
        ("iov_base", ctypes.c_void_p),
        ("iov_len", ctypes.c_ulong),
    )


if __name__ == "__main__":
    import os

    bytes1 = ctypes.c_byte(1)
    bytes2 = (ctypes.c_byte * 3)(20, 21, 22)
    bufs = process_vm_readv(
        os.getpid(),
        [(ctypes.addressof(bytes1), 1), (ctypes.addressof(bytes2), 3)],
    )
    print(bufs)
