#!/usr/bin/env python3
"""Scenario E: the life of a session.

Created detached, attached, detached on purpose, re-attached,
renamed -- then two different deaths: kill-session, which is
final, and a killed server, which leaves the session
resurrectable. Deletion, refused and forced, ends the tour.
"""
import os
import signal
import subprocess
import time

from drive import Client, clean_slate, run, show, wait_session


def server_pid(name):
    out = subprocess.run(["pgrep", "-af", "zellij --server"],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.rstrip().endswith(f"/{name}"):
            return int(line.split()[0])
    return None


def wait_pane(name, timeout=12):
    end = time.time() + timeout
    while time.time() < end:
        rc, out = run(["--session", name, "action", "list-panes"])
        if "terminal_0" in out:
            return out
        time.sleep(0.5)
    return out


def detach(client):
    """Ctrl o, then d, and wait for the client process to go.
    Retried once: an overlay pane can eat the first attempt,
    and on a shared machine the exit can take a moment."""
    for _ in range(2):
        client.type("\x1b", settle=0.5)   # dismiss any overlay
        client.type("\x0f", settle=0.5)   # Ctrl o: Session mode
        client.type("d", settle=0.5)      # d: detach
        for _ in range(12):
            if not client.alive():
                return True
            client.pump(0.5)
    return not client.alive()


clean_slate()

# --- created in the background, no client anywhere --------------
rc, out = run(["attach", "lab-life", "--create-background"])
show("zellij attach lab-life --create-background", rc, out)
wait_session("lab-life")
rc, out = run(["list-sessions"])
show("zellij list-sessions", rc, out)
out = wait_pane("lab-life")
show("zellij --session lab-life action list-panes", 0, out)
print("[the session and its panes exist with nobody attached]\n")

# --- attach, leave a marker, detach with the keys ---------------
client = Client(["attach", "lab-life"])
client.pump(2.5)
client.type("\x1b", settle=0.6)  # dismiss any overlay pane
client.type("echo marker-before-detach\r", settle=1.0)
print("[attached, and typed: echo marker-before-detach]\n")
gone = detach(client)
print("[pressed Ctrl o, then d -- detach]\n")
print(f"[client detached and gone: {gone}]\n")
rc, out = run(["list-sessions"])
show("zellij list-sessions   (after detaching)", rc, out)
client.stop()

# --- re-attach: the shell never died -----------------------------
client = Client(["attach", "lab-life"])
client.pump(2.5)
rc, out = run(["--session", "lab-life", "action", "dump-screen"])
show("zellij --session lab-life action dump-screen   "
     "(after re-attaching)", rc, out)

# Rename the session itself from outside.
rc, out = run(["--session", "lab-life", "action", "rename-session",
               "lab-renamed"])
show("zellij --session lab-life action rename-session lab-renamed",
     rc, out)
rc, out = run(["list-sessions"])
show("zellij list-sessions", rc, out)
client.stop()

# --- death one: kill-session is final ----------------------------
rc, out = run(["kill-session", "lab-renamed"])
show("zellij kill-session lab-renamed", rc, out)
rc, out = run(["list-sessions"])
show("zellij list-sessions   (after the kill)", rc, out)
print("[gone entirely: a session you kill on purpose is not "
      "kept for resurrection]\n")

# --- death two: the server dies without being asked --------------
client = Client(["--session", "lab-crash"])
wait_session("lab-crash")
client.pump(2.5)
client.type("\x1b", settle=0.6)
client.type("\x1bn", settle=1.0)  # Alt n: a second pane
# Rename the tab with the keys a user would use: Ctrl t for
# Tab mode, r for rename, type the name, Enter.
client.type("\x14", settle=0.5)
client.type("r", settle=0.5)
client.type("Keepsake\r", settle=1.0)
print("[renamed the tab to Keepsake with Ctrl t, r]\n")
out = wait_pane("lab-crash")
show("zellij --session lab-crash action list-panes   "
     "(two terminal panes)", 0, out)
# Resurrection works from saved state. Zellij saves on an
# interval; save-session forces a save right now, so the kill
# below has something to resurrect from.
rc, out = run(["--session", "lab-crash", "action", "save-session"])
show("zellij --session lab-crash action save-session", rc, out)
info = os.path.expanduser(
    "~/.cache/zellij/contract_version_1/session_info/lab-crash")
names = sorted(os.listdir(info))
print(f"[the saved state lives in {info}:]\n")
for n in names:
    print(" ", n)
layout_file = os.path.join(info, "session-layout.kdl")
print("\n[session-layout.kdl begins:]\n")
with open(layout_file) as fh:
    for line in fh.read().splitlines()[:9]:
        print(line)
print()
pid = server_pid("lab-crash")
print(f"[the server for lab-crash is process {pid}; "
      "killing it with SIGKILL -- no cleanup, no warning]\n")
os.kill(pid, signal.SIGKILL)
time.sleep(1.5)
client.stop()
rc, out = run(["list-sessions"])
show("zellij list-sessions   (after the server's death)", rc, out)

# --- resurrection --------------------------------------------------
client = Client(["attach", "lab-crash"])
client.pump(3.0)
print("[attached to the dead session -- it resurrects]\n")
rc, out = run(["--session", "lab-crash", "action", "list-tabs"])
show("zellij --session lab-crash action list-tabs", rc, out)
rc, out = run(["--session", "lab-crash", "action", "list-panes"])
show("zellij --session lab-crash action list-panes", rc, out)
rc, out = run(["--session", "lab-crash", "action", "dump-screen"])
show("zellij ... action dump-screen   (a resurrected pane)",
     rc, out)
print("[the layout and the tab's name came back; the shells are "
      "fresh -- what was on their screens is not part of what is "
      "saved by default]\n")
client.type("\x11", settle=1.0)
client.stop()
clean_slate()

# --- deletion, refused and forced ----------------------------------
rc, out = run(["attach", "lab-doomed", "--create-background"])
wait_session("lab-doomed")
rc, out = run(["delete-session", "lab-doomed"])
show("zellij delete-session lab-doomed   (still running)", rc, out)
rc, out = run(["delete-session", "--force", "lab-doomed"])
show("zellij delete-session --force lab-doomed", rc, out)
rc, out = run(["delete-session", "lab-doomed"])
show("zellij delete-session lab-doomed   (already gone)", rc, out)
rc, out = run(["list-sessions"])
show("zellij list-sessions   (at the end)", rc, out)
