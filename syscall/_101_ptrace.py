import errno
import ctypes
import typing

from .common import libc

__all__ = [
    "PTRACE_ATTACH",
    "PTRACE_DETACH",
    "PTRACE_GETREGS",
    "PTRACE_SETREGS",
    "PTRACE_PEEKDATA",
    "PTRACE_POKEDATA",
    "PTRACE_SINGLESTEP",
    "PTRACE_CONT",
    "ptrace",
    "UserRegsStruct",
]

PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_GETREGS = 12
PTRACE_SETREGS = 13
PTRACE_PEEKDATA = 2
PTRACE_POKEDATA = 5
PTRACE_SINGLESTEP = 9
PTRACE_CONT = 7


libc.ptrace.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes.c_void_p,
]


def ptrace(request: int, pid: int, addr: int, data: typing.Any) -> int:
    """
    long ptrace(enum __ptrace_request request, pid_t pid, void *addr, void *data); # noqa
    """
    if data:
        data = ctypes.pointer(data)
    res = libc.ptrace(request, pid, addr, data)
    if res == -1:
        raise OSError(errno.errorcode[ctypes.get_errno()])
    return res


ptrace.syscall_no = 101


class UserRegsStruct(ctypes.Structure):
    """
    struct user_regs_struct
    {
      __extension__ unsigned long long int r15;
      __extension__ unsigned long long int r14;
      __extension__ unsigned long long int r13;
      __extension__ unsigned long long int r12;
      __extension__ unsigned long long int rbp;
      __extension__ unsigned long long int rbx;
      __extension__ unsigned long long int r11;
      __extension__ unsigned long long int r10;
      __extension__ unsigned long long int r9;
      __extension__ unsigned long long int r8;
      __extension__ unsigned long long int rax;
      __extension__ unsigned long long int rcx;
      __extension__ unsigned long long int rdx;
      __extension__ unsigned long long int rsi;
      __extension__ unsigned long long int rdi;
      __extension__ unsigned long long int orig_rax;
      __extension__ unsigned long long int rip;
      __extension__ unsigned long long int cs;
      __extension__ unsigned long long int eflags;
      __extension__ unsigned long long int rsp;
      __extension__ unsigned long long int ss;
      __extension__ unsigned long long int fs_base;
      __extension__ unsigned long long int gs_base;
      __extension__ unsigned long long int ds;
      __extension__ unsigned long long int es;
      __extension__ unsigned long long int fs;
      __extension__ unsigned long long int gs;
    };
    """

    _fields_ = (
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
        ("r8", ctypes.c_ulonglong),
        ("rax", ctypes.c_ulonglong),
        ("rcx", ctypes.c_ulonglong),
        ("rdx", ctypes.c_ulonglong),
        ("rsi", ctypes.c_ulonglong),
        ("rdi", ctypes.c_ulonglong),
        ("orig_rax", ctypes.c_ulonglong),
        ("rip", ctypes.c_ulonglong),
        ("cs", ctypes.c_ulonglong),
        ("eflags", ctypes.c_ulonglong),
        ("rsp", ctypes.c_ulonglong),
        ("ss", ctypes.c_ulonglong),
        ("fs_base", ctypes.c_ulonglong),
        ("gs_base", ctypes.c_ulonglong),
        ("ds", ctypes.c_ulonglong),
        ("es", ctypes.c_ulonglong),
        ("fs", ctypes.c_ulonglong),
        ("gs", ctypes.c_ulonglong),
    )


if __name__ == "__main__":
    import os
    import sys

    pid = int(sys.argv[1])
    ptrace(PTRACE_ATTACH, pid, 0, 0)
    os.wait()
    regs = UserRegsStruct()
    ptrace(PTRACE_GETREGS, pid, 0, regs)
    ptrace(PTRACE_SETREGS, pid, 0, regs)
    print(regs.rip)
    ptrace(PTRACE_DETACH, pid, 0, 0)
