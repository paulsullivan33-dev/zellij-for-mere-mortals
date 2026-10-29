#!/usr/bin/env python3
"""Scenario B: panes and tabs, driven with real keystrokes.

Uses the keyboard the way a reader would (Ctrl p, then a
letter) and inspects the result with action commands.
"""
import time

from drive import Client, clean_slate, run, show, wait_session

NAME = "lab-panes"
clean_slate()
client = Client(["--session", NAME])
wait_session(NAME)
client.pump(2.5)
client.type("\x1b", settle=0.8)  # dismiss the About pane
print("[session started; About pane dismissed with ESC]\n")

client.type("echo first-pane-here\r", settle=1.0)
print("[typed in pane 1: echo first-pane-here]\n")

# Ctrl p enters Pane mode; r splits to the right.
client.type("\x10", settle=0.5)
client.type("r", settle=1.2)
print("[pressed Ctrl p, then r -- a new pane opens to the right, "
      "and focus moves to it]\n")

client.type("echo second-pane-here\r", settle=1.0)
print("[typed in pane 2: echo second-pane-here]\n")

rc, out = run(["--session", NAME, "action", "list-panes"])
show(f"zellij --session {NAME} action list-panes", rc, out)

rc, out = run(["--session", NAME, "action", "dump-screen",
               "--pane-id", "terminal_0"])
show("zellij ... action dump-screen --pane-id terminal_0", rc, out)
rc, out = run(["--session", NAME, "action", "dump-screen",
               "--pane-id", "terminal_1"])
show("zellij ... action dump-screen --pane-id terminal_1", rc, out)

rc, out = run(["--session", NAME, "action", "dump-layout"])
show(f"zellij --session {NAME} action dump-layout", rc, out)

# Ctrl t enters Tab mode; n opens a new tab.
client.type("\x14", settle=0.5)
client.type("n", settle=1.2)
print("[pressed Ctrl t, then n -- a second tab opens]\n")
client.type("echo second-tab-here\r", settle=1.0)
print("[typed in tab 2: echo second-tab-here]\n")

rc, out = run(["--session", NAME, "action", "list-tabs"])
show(f"zellij --session {NAME} action list-tabs", rc, out)
rc, out = run(["--session", NAME, "action", "query-tab-names"])
show(f"zellij --session {NAME} action query-tab-names", rc, out)

# Rename the tab from outside, then close the first pane.
rc, out = run(["--session", NAME, "action", "rename-tab", "Second"])
show("zellij ... action rename-tab Second", rc, out)
rc, out = run(["--session", NAME, "action", "query-tab-names"])
show("zellij ... action query-tab-names   (after the rename)", rc, out)

client.type("\x11", settle=1.0)  # Ctrl q
print("[sent Ctrl q]")
client.stop()
