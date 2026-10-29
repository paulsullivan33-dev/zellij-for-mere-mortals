#!/usr/bin/env python3
"""Scenario D: configuration files.

Puts a config in the default location and checks it three
ways: setup --check finds it, a new session obeys it (no
release-notes pane appears, and a keybind added by the file
works), and two broken configs produce their errors.
"""
import os
import shutil

from drive import Client, clean, clean_slate, run, show, wait_session

LAB = os.path.dirname(os.path.abspath(__file__))
GOOD = os.path.join(LAB, "configs", "good.kdl")
UNKNOWN = os.path.join(LAB, "configs", "unknown-key.kdl")
SYNTAX = os.path.join(LAB, "configs", "syntax-error.kdl")
DEST = os.path.expanduser("~/.config/zellij/config.kdl")

clean_slate()
os.makedirs(os.path.dirname(DEST), exist_ok=True)
if os.path.exists(DEST):
    os.remove(DEST)

rc, out = run(["setup", "--check"])
lines = [l for l in out.splitlines() if "CONFIG" in l]
print("$ zellij setup --check   (config lines only, before)\n")
print("\n".join(lines[:4]))
print()
shutil.copy(GOOD, DEST)
print(f"[wrote the lab config to {DEST}:]\n")
print(open(GOOD).read())

rc, out = run(["setup", "--check"])
lines = [l for l in out.splitlines() if "CONFIG" in l]
print("$ zellij setup --check   (config lines only, after)\n")
print("\n".join(lines[:4]))
print()

# --- behaviour: a session under this config ---------------------
client = Client(["--session", "lab-config"])
wait_session("lab-config")
client.pump(2.5)
rc, out = run(["--session", "lab-config", "action", "list-panes"])
show("zellij --session lab-config action list-panes", rc, out)
print("[no About or Release Notes pane: show_release_notes "
      "false did its job -- compare scenario A, where one "
      "appeared]\n")

# Split with Alt n (a default bind), then close with Alt w
# (the bind this config added -- it is not a default).
client.type("\x1bn", settle=1.2)
rc, out = run(["--session", "lab-config", "action", "list-panes"])
show("... list-panes   (after Alt n, the new-pane key)", rc, out)
client.type("\x1bw", settle=1.2)
rc, out = run(["--session", "lab-config", "action", "list-panes"])
show("... list-panes   (after Alt w, the config's own key)", rc, out)
client.type("\x11", settle=1.0)
client.stop()
clean_slate()

# --- broken configs ----------------------------------------------
# An unknown key is not an error at all: the check passes and a
# session starts happily. A typo in a config is therefore silent.
rc, out = run(["--config", UNKNOWN, "setup", "--check"])
keep = [l for l in out.splitlines() if "CONFIG FILE" in l]
print("$ zellij --config configs/unknown-key.kdl setup --check\n")
print("\n".join(keep))
print("\n[banana_mode true is not a zellij option -- and nothing "
      "complains. Unknown keys are ignored.]\n")

# A syntax error, by contrast, is loud and precise.
rc, out = run(["--config", SYNTAX, "setup", "--check"])
show("zellij --config configs/syntax-error.kdl setup --check",
     rc, out)

client = Client(["--config", SYNTAX, "--session", "lab-badcfg"])
client.pump(3.0)
print("[starting a session with that config prints the same "
      "diagnostic, and:]\n")
rc, out = run(["list-sessions"])
show("zellij list-sessions", rc, out)
client.stop()
clean_slate()

os.remove(DEST)
print("[removed the lab config from the default location]")
