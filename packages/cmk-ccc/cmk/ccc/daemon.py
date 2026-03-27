#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import os
import sys
from collections.abc import Generator
from contextlib import contextmanager, suppress
from pathlib import Path

from cmk.ccc import store
from cmk.ccc.exceptions import MKGeneralException


def daemonize() -> None:
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork failed (#1): {e.errno} ({e.strerror})\n")
        sys.exit(1)

    # decouple from parent environment
    # chdir -> don't prevent unmounting...
    os.chdir("/")

    # Create new process group with the process as leader
    os.setsid()

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Fork failed (#2): {e.errno} ({e.strerror})\n")
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

    si = os.open("/dev/null", os.O_RDONLY)
    so = os.open("/dev/null", os.O_WRONLY)
    os.dup2(si, 0)
    os.dup2(so, 1)
    os.dup2(so, 2)
    os.close(si)
    os.close(so)


def closefrom(lowfd: int) -> None:
    """Closes all file descriptors starting with "lowfd", ignoring errors

    Deletes all open file descriptors greater than or equal to lowfd from the
    per-process object reference table.  Any errors encountered while closing
    file descriptors are ignored.

    Difference to os.closerange() is that this automatically determines the
    highest fd number to close.
    """
    try:
        highfd = os.sysconf("SC_OPEN_MAX")
    except ValueError:
        highfd = 1024

    os.closerange(lowfd, highfd)


@contextmanager
def pid_file_lock(path: Path) -> Generator[None]:
    """Context manager for PID file based locking"""
    if not store.try_acquire_lock(path):
        raise MKGeneralException(
            "Failed to acquire PID file lock: Another process is already running"
        )
    # Now that we have the lock we are allowed to write our pid to the file.
    # The pid can then be used by the init script.
    with path.open("w", encoding="utf-8") as f:
        f.write(f"{os.getpid()}\n")
    try:
        yield
    finally:
        store.release_lock(path)
        with suppress(OSError):
            path.unlink()
