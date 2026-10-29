#!/usr/bin/env python3
"""Scenario G: modes at the keyboard.

Scroll mode over a long output, and locked mode: proof that
while locked, the pane-mode keys do nothing to the layout and
every key reaches the program in the pane.
"""
from drive import Client, clean_slate, run, show, wait_session

NAME = "lab-modes"
clean_slate()
client = Client(["--session", NAME])
wait_session(NAME)
client.pump(2.5)
client.type("\x1b", settle=0.6)  # dismiss the About pane

client.type("seq 1 60\r", settle=1.2)
print("[ran: seq 1 60 -- sixty numbered lines]\n")
rc, out = run(["--session", NAME, "action", "dump-screen"])
show("zellij ... action dump-screen   (the tail of the output)",
     rc, out)

client.type("\x13", settle=0.5)  # Ctrl s: Scroll mode
client.type("gg", settle=0.3)    # (not bound here; harmless)
client.type("\x02\x02", settle=1.0)  # Ctrl b twice: two pages up
print("[pressed Ctrl s for Scroll mode, then Ctrl b twice -- "
      "two pages back through the output]\n")
rc, out = run(["--session", NAME, "action", "dump-screen"])
show("zellij ... action dump-screen   (scrolled up)", rc, out)
client.type("\x03", settle=0.8)  # Ctrl c: to the bottom, Normal
print("[pressed Ctrl c -- back to the bottom and Normal mode]\n")

# --- locked mode ---------------------------------------------------
client.type("\x07", settle=0.5)  # Ctrl g: Locked mode
client.type("\x10", settle=0.3)  # Ctrl p -- would open Pane mode
client.type("r", settle=0.8)     # r -- would split to the right
print("[locked with Ctrl g, then pressed Ctrl p, r -- the keys "
      "pane mode would have used to split]\n")
rc, out = run(["--session", NAME, "action", "list-panes"])
show("zellij ... action list-panes   (still locked)", rc, out)
client.type("\x03", settle=0.4)  # Ctrl c clears the shell's line
client.type("echo typed-while-locked\r", settle=1.0)
print("[typed a command while still locked -- it went to the "
      "shell, as every key does in this mode]\n")
rc, out = run(["--session", NAME, "action", "dump-screen"])
show("zellij ... action dump-screen", rc, out)

client.type("\x07", settle=0.5)  # Ctrl g: back to Normal
client.type("\x10", settle=0.4)  # Ctrl p: Pane mode
client.type("r", settle=1.2)     # r: the same split, now it works
print("[unlocked with Ctrl g, pressed Ctrl p, r again]\n")
rc, out = run(["--session", NAME, "action", "list-panes"])
show("zellij ... action list-panes   (unlocked)", rc, out)

client.type("\x11", settle=1.0)
client.stop()
clean_slate()
