import errno
import ctypes

from .common import libc, Structure, raise_on


class Sigset(Structure):
    """
    typedef struct {
        unsigned long sig[_NSIG_WORDS];
    } sigset_t;
    """

    NSIG_WORDS = int(1024 / (8 * ctypes.sizeof(ctypes.c_ulong)))

    _fields_ = (("sig", ctypes.c_ulong * NSIG_WORDS),)


@raise_on(lambda rv: rv != 0)
def sigemptyset(sigset: Sigset) -> int:
    """
    int sigemptyset(sigset_t *set);
    """
    return libc.sigemptyset(sigset.byref())


@raise_on(lambda rv: rv != 0)
def sigaddset(sigset: Sigset, signo: int) -> int:
    """
    int sigaddset(sigset_t *set);
    """
    res = libc.sigaddset(sigset.byref(), signo)
    if res != 0:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res


@raise_on(lambda rv: rv == -1)
def sigismember(sigset: Sigset, signo: int) -> int:
    """
    int sigismember(const sigset_t *set, int signum)
    """
    return libc.sigismember(sigset.byref(), signo)
