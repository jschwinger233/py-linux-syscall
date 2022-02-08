import errno
import ctypes

from .common import libc


class Sigset(ctypes.Structure):
    """
    typedef struct {
        unsigned long sig[_NSIG_WORDS];
    } sigset_t;
    """

    _fields_ = (("sig", ctypes.c_ulong * 2),)


def sigemptyset(sigset: Sigset) -> int:
    """
    int sigemptyset(sigset_t *set);
    """
    res = libc.sigemptyset(ctypes.pointer(sigset))
    if res != 0:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res


def sigaddset(sigset: Sigset, signo: int) -> int:
    """
    int sigaddset(sigset_t *set);
    """
    res = libc.sigaddset(ctypes.pointer(sigset), signo)
    if res != 0:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res


def sigismember(sigset: Sigset, signo: int) -> bool:
    """
    int sigismember(const sigset_t *set, int signum)
    """
    res = libc.sigismember(ctypes.pointer(sigset), signo)
    if res == -1:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res == 1
