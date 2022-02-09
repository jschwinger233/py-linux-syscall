import errno
import signal
import ctypes

from ._0_read import read

from .common import libc
from .signal_common import Sigset, sigemptyset, sigaddset

__all__ = ["SFD_CLOEXEC", "SFD_NONBLOCK", "signalfd", "SignalfdSiginfo"]

SFD_CLOEXEC = 0o2000000
SFD_NONBLOCK = 0o4000

libc.signalfd.argtypes = [ctypes.c_int, ctypes.POINTER(Sigset), ctypes.c_int]
libc.signalfd.restype = ctypes.c_int


def signalfd(fd: int, signos: [int], flags: int) -> int:
    """
    int signalfd(int fd, const sigset_t *mask, int flags);
    """
    sigset = Sigset()
    sigemptyset(sigset)
    for signo in signos:
        sigaddset(sigset, signo)
    res = libc.signalfd(fd, ctypes.pointer(sigset), flags)
    if res == -1:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res


signalfd.no = 282


class SignalfdSiginfo(ctypes.Structure):
    """
    struct signalfd_siginfo {
        uint32_t ssi_signo;    /* Signal number */
        int32_t  ssi_errno;    /* Error number (unused) */
        int32_t  ssi_code;     /* Signal code */
        uint32_t ssi_pid;      /* PID of sender */
        uint32_t ssi_uid;      /* Real UID of sender */
        int32_t  ssi_fd;       /* File descriptor (SIGIO) */
        uint32_t ssi_tid;      /* Kernel timer ID (POSIX timers)
        uint32_t ssi_band;     /* Band event (SIGIO) */
        uint32_t ssi_overrun;  /* POSIX timer overrun count */
        uint32_t ssi_trapno;   /* Trap number that caused signal */
        int32_t  ssi_status;   /* Exit status or signal (SIGCHLD) */
        int32_t  ssi_int;      /* Integer sent by sigqueue(3) */
        uint64_t ssi_ptr;      /* Pointer sent by sigqueue(3) */
        uint64_t ssi_utime;    /* User CPU time consumed (SIGCHLD) */
        uint64_t ssi_stime;    /* System CPU time consumed
                                  (SIGCHLD) */
        uint64_t ssi_addr;     /* Address that generated signal
                                  (for hardware-generated signals) */
        uint16_t ssi_addr_lsb; /* Least significant bit of address
                                  (SIGBUS; since Linux 2.6.37)
        uint8_t  pad[X];       /* Pad size to 128 bytes (allow for
                                  additional fields in the future) */
    """

    _fields_ = (
        ("ssi_signo", ctypes.c_uint32),
        ("ssi_errno", ctypes.c_int32),
        ("ssi_code", ctypes.c_int32),
        ("ssi_pid", ctypes.c_uint32),
        ("ssi_uid", ctypes.c_uint32),
        ("ssi_fd", ctypes.c_int32),
        ("ssi_tid", ctypes.c_uint32),
        ("ssi_bandn", ctypes.c_uint32),
        ("ssi_overrun", ctypes.c_uint32),
        ("ssi_trapno", ctypes.c_uint32),
        ("ssi_status", ctypes.c_int32),
        ("ssi_int", ctypes.c_int32),
        ("ssi_ptr", ctypes.c_uint64),
        ("ssi_utime", ctypes.c_uint64),
        ("ssi_stime", ctypes.c_uint64),
        ("ssi_addr", ctypes.c_uint64),
        ("ssi_addr_lsb", ctypes.c_uint16),
        ("pad", ctypes.c_uint8 * 46),
    )


if __name__ == "__main__":
    signos = [signal.SIGINT, signal.SIGQUIT]
    signal.pthread_sigmask(signal.SIG_BLOCK, signos)
    flags = SFD_CLOEXEC
    fd = signalfd(-1, signos, flags)
    siginfo = SignalfdSiginfo()
    while 1:
        n = read(fd, siginfo, 128)
        if n != ctypes.sizeof(siginfo):
            raise RuntimeError("read")

        if siginfo.ssi_signo == signal.SIGINT:
            print("got SIGINT")
        elif siginfo.ssi_signo == signal.SIGQUIT:
            print("got SIGQUIT")
            break
        else:
            print("read unexpected signal")
