#!/usr/bin/env python3
"""Scenario C: layouts from files.

Starts sessions from layout files, compares a layout with and
without a default tab template, adds a tab to a running session
from a second layout file, feeds zellij a broken layout, loads
a layout by name from the layout directory, and finally
round-trips: dump a running session's layout and start a new
session from the dump.

Note the flag that matters: a new session takes its layout via
--new-session-with-layout. Plain --layout together with
--session means "add these tabs to that running session" --
with no such session, zellij answers "There is no active
session!" (the lab's first attempt did exactly this).
"""
import os
import time

from drive import Client, clean, clean_slate, run, show, wait_session

LAB = os.path.dirname(os.path.abspath(__file__))
PLAIN = os.path.join(LAB, "layouts", "workbench.kdl")
BARS = os.path.join(LAB, "layouts", "workbench-with-bars.kdl")
EXTRA = os.path.join(LAB, "layouts", "extra-tab.kdl")
BROKEN = os.path.join(LAB, "layouts", "broken.kdl")

clean_slate()

# --- 1. a plain layout file -------------------------------------
client = Client(["--session", "lab-layout",
                 "--new-session-with-layout", PLAIN])
wait_session("lab-layout")
client.pump(2.5)
print("[started: zellij --session lab-layout "
      "--new-session-with-layout layouts/workbench.kdl]\n")
rc, out = run(["--session", "lab-layout", "action", "list-tabs"])
show("zellij --session lab-layout action list-tabs", rc, out)
rc, out = run(["--session", "lab-layout", "action", "list-panes"])
show("zellij --session lab-layout action list-panes", rc, out)
rc, dumped = run(["--session", "lab-layout", "action", "dump-layout"])
print("[the head of action dump-layout for this session:]\n")
for line in dumped.rstrip().splitlines()[:7]:
    print(line)
print("\n[note: the tab holds one bare pane -- no tab-bar or "
      "status-bar, because the layout did not ask for them]\n")

# --- 2. add a tab to the running session from another file -----
rc, out = run(["--session", "lab-layout", "--layout", EXTRA])
time.sleep(1.5)
print("[meanwhile, from a second shell: zellij --session "
      "lab-layout --layout layouts/extra-tab.kdl]\n")
rc, out = run(["--session", "lab-layout", "action", "list-tabs"])
show("zellij --session lab-layout action list-tabs   "
     "(after the add)", rc, out)
client.type("\x11", settle=1.0)
client.stop()
clean_slate()

# --- 3. the same layout with a default tab template -------------
client = Client(["--session", "lab-bars",
                 "--new-session-with-layout", BARS])
wait_session("lab-bars")
client.pump(2.5)
print("[started again with workbench-with-bars.kdl, which adds "
      "a default_tab_template]\n")
rc, out = run(["--session", "lab-bars", "action", "list-panes"])
show("zellij --session lab-bars action list-panes", rc, out)
print("[list-panes looks the same -- with a client attached, "
      "the two bars are the client's own rendering and are not "
      "listed. The difference shows in the dump-layout below: "
      "each tab now carries a tab-bar and a status-bar pane, "
      "from the template]\n")

rc, out = run(["--session", "lab-bars", "action", "go-to-tab-name",
               "Worker"])
time.sleep(1.0)
rc, out = run(["--session", "lab-bars", "action", "dump-screen"])
show("zellij ... action dump-screen   (the Worker tab)", rc, out)

# --- 4. round-trip the layout of the running session ------------
dumped = ""
for _attempt in range(5):
    rc, dumped = run(["--session", "lab-bars", "action",
                      "dump-layout"])
    if dumped.strip():
        break
    time.sleep(1.0)
dump_path = os.path.join(LAB, "layouts", "round-trip.kdl")
with open(dump_path, "w") as fh:
    fh.write(dumped)
lines = dumped.rstrip().splitlines()
print(f"[saved action dump-layout to layouts/round-trip.kdl "
      f"({len(lines)} lines); its head reads:]\n")
for line in lines[:8]:
    print(line)
print()
client.type("\x11", settle=1.0)
client.stop()
clean_slate()

client = Client(["--session", "lab-roundtrip",
                 "--new-session-with-layout", dump_path])
wait_session("lab-roundtrip")
client.pump(2.5)
print("[started a new session from the dumped layout]\n")
rc, out = run(["--session", "lab-roundtrip", "action", "list-tabs"])
show("zellij --session lab-roundtrip action list-tabs", rc, out)
client.type("\x11", settle=1.0)
client.stop()
clean_slate()

# --- 5. a broken layout ------------------------------------------
client = Client(["--session", "lab-broken",
                 "--new-session-with-layout", BROKEN])
client.pump(3.0)
print("[started with layouts/broken.kdl (a missing closing "
      "brace); the client printed:]\n")
text = clean(bytes(client.output).decode("utf-8", "replace"))
for line in text.splitlines():
    if line.strip():
        print(line.rstrip())
print(f"\n[client still running: {client.alive()}]")
client.stop()
rc, out = run(["list-sessions"])
show("zellij list-sessions   (after the broken layout)", rc, out)
clean_slate()

# --- 6. a layout by name, from the layout directory --------------
layout_dir = os.path.expanduser("~/.config/zellij/layouts")
os.makedirs(layout_dir, exist_ok=True)
dest = os.path.join(layout_dir, "workbench.kdl")
with open(BARS) as fh, open(dest, "w") as out_fh:
    out_fh.write(fh.read())
print(f"[copied the with-bars layout to {dest}]\n")
client = Client(["--session", "lab-byname",
                 "--new-session-with-layout", "workbench"])
wait_session("lab-byname")
client.pump(2.5)
print("[started: zellij --session lab-byname "
      "--new-session-with-layout workbench (a name, not a path)]\n")
rc, out = run(["--session", "lab-byname", "action", "list-tabs"])
show("zellij --session lab-byname action list-tabs", rc, out)
client.type("\x11", settle=1.0)
client.stop()
clean_slate()
