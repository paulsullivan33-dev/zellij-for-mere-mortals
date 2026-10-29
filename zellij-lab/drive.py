#!/usr/bin/env python3
"""Drive a real Zellij client in a pseudo-terminal.

The lab has no human at a keyboard, so this script plays the
human: it starts a Zellij client attached to a pty of a known
size, types into it, reads what the client paints, and leaves
the server running for inspection by other commands.

Usage: imported by the scenario scripts in this directory.
"""

import fcntl
import os
import pty
import select
import struct
import subprocess
import sys
import termios
import time

ZELLIJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tool", "zellij")


class Client:
    def __init__(self, args, cols=110, rows=32, env_extra=None):
        self.master, slave = pty.openpty()
        # Set the window size before the client starts, so its
        # first paint is already at the size we want to inspect.
        fcntl.ioctl(slave, termios.TIOCSWINSZ,
                    struct.pack("HHHH", rows, cols, 0, 0))
        env = dict(os.environ)
        env["TERM"] = "xterm-256color"
        env["LC_ALL"] = "C.UTF-8"
        env.pop("ZELLIJ", None)
        env.pop("ZELLIJ_SESSION_NAME", None)
        env.pop("ZELLIJ_PANE_ID", None)
        if env_extra:
            env.update(env_extra)
        self.proc = subprocess.Popen(
            [ZELLIJ] + args,
            stdin=slave, stdout=slave, stderr=slave,
            env=env, close_fds=True)
        os.close(slave)
        os.set_blocking(self.master, False)
        self.output = bytearray()

    def pump(self, seconds=0.4):
        """Read whatever the client paints for `seconds`."""
        end = time.time() + seconds
        while time.time() < end:
            r, _, _ = select.select([self.master], [], [], 0.1)
            if self.master in r:
                try:
                    chunk = os.read(self.master, 65536)
                except OSError:
                    break
                if not chunk:
                    break
                self.output.extend(chunk)
        return self

    def wait_for(self, needle, timeout=15):
        """Wait until `needle` (bytes) appears in the output."""
        end = time.time() + timeout
        while time.time() < end:
            self.pump(0.3)
            if needle in self.output:
                return True
        return needle in self.output

    def type(self, text, settle=0.5):
        os.write(self.master, text.encode())
        self.pump(settle)
        return self

    def alive(self):
        return self.proc.poll() is None

    def stop(self):
        if self.alive():
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=5)
        os.close(self.master)


def run(args, timeout=30, **kw):
    """Run a non-interactive zellij command; return (rc, text)."""
    env = dict(os.environ)
    env.pop("ZELLIJ", None)
    env.pop("ZELLIJ_SESSION_NAME", None)
    env.pop("ZELLIJ_PANE_ID", None)
    proc = subprocess.run([ZELLIJ] + args, capture_output=True,
                          text=True, env=env, timeout=timeout, **kw)
    return proc.returncode, (proc.stdout + proc.stderr)


def wait_session(name, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        rc, out = run(["list-sessions"])
        if name in out:
            return True
        time.sleep(0.5)
    return False


import re

_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")


def clean(text):
    """Strip ANSI escapes so transcripts read as plain text."""
    return _ANSI.sub("", text)


def show(cmd_text, rc, out):
    print(f"$ {cmd_text}")
    print(clean(out).rstrip())
    print(f"[exit {rc}]")
    print()
    sys.stdout.flush()


def clean_slate():
    """Kill every live session and delete every dead one.

    The *-all-sessions commands ask for confirmation; without
    --yes (and without a terminal) they die on the prompt, so
    the lab always passes --yes.
    """
    run(["kill-all-sessions", "--yes"])
    run(["delete-all-sessions", "--yes", "--force"])
    time.sleep(0.5)
