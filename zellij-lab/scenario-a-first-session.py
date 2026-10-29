#!/usr/bin/env python3
"""Scenario A: a first session, driven through a pty.

Starts a client, types a command into its pane, inspects the
session from a second shell, then quits with Ctrl q.
"""
import sys
import time

from drive import Client, clean_slate, run, show, wait_session

NAME = "lab-first"

clean_slate()
rc, out = run(["list-sessions"])
show("zellij list-sessions   (before anything starts)", rc, out)

client = Client(["--session", NAME])
print(f"[started a client in a pty: zellij --session {NAME}]")
ok = wait_session(NAME)
print(f"[session visible to list-sessions: {ok}]")
client.pump(2.5)

rc, out = run(["--session", NAME, "action", "list-panes"])
show(f"zellij --session {NAME} action list-panes", rc, out)

# A first run opens a Release Notes pane over the terminal.
# Its own footer says ESC dismisses it; a user would do this.
client.type("\x1b", settle=1.0)
print("[pressed ESC -- the release-notes pane closes, "
      "the terminal pane takes focus]\n")

rc, out = run(["list-sessions"])
show("zellij list-sessions", rc, out)

client.type("echo hello-from-the-first-pane\r", settle=1.2)
print("[typed into the pane: echo hello-from-the-first-pane]\n")

rc, out = run(["--session", NAME, "action", "dump-screen"])
show(f"zellij --session {NAME} action dump-screen", rc, out)

client.type("\x11", settle=1.5)  # Ctrl q quits zellij
print("[sent Ctrl q -- the quit key]\n")
time.sleep(1.0)
print(f"[client process still running: {client.alive()}]")
rc, out = run(["list-sessions"])
show("zellij list-sessions   (after quitting)", rc, out)
client.stop()
