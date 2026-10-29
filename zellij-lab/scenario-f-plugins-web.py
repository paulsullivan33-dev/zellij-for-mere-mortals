#!/usr/bin/env python3
"""Scenario F: plugins and the web server.

Plugin aliases, the built-in plugins on disk, the session
manager opened with its keys in a live session, and the web
server: started, questioned with curl, and stopped. (Driving
the web client in a browser is beyond this lab.)
"""
import os
import re
import shutil
import subprocess
import time

from drive import Client, clean_slate, run, show, wait_session

LAB = os.path.dirname(os.path.abspath(__file__))


def cur(proc):
    return proc.stdout.strip()

rc, out = run(["list-aliases"])
show("zellij list-aliases", rc, out)

dump_dir = os.path.join(LAB, "plugin-dump")
rc, out = run(["setup", "--dump-plugins", dump_dir])
show("zellij setup --dump-plugins zellij-lab/plugin-dump", rc, out)
print("[the directory then holds (in a plugins/ folder):]\n")
for root, _dirs, files in os.walk(dump_dir):
    for name in sorted(files):
        size = os.path.getsize(os.path.join(root, name))
        print(f"  {name}  ({size} bytes)")
print()
shutil.rmtree(dump_dir)
print("[the lab deleted the dumped copies again -- the "
      "listing above is the evidence]\n")

# --- the session manager, with its keys ---------------------------
clean_slate()
run(["attach", "lab-other", "--create-background"])
client = Client(["--session", "lab-f1"])
wait_session("lab-f1")
client.pump(2.5)
client.type("\x1b", settle=0.6)
client.type("\x0f", settle=0.5)  # Ctrl o: Session mode
client.type("w", settle=2.0)     # w: session manager
print("[in session lab-f1, pressed Ctrl o, then w -- the "
      "session manager opens as a floating pane]\n")
rc, out = run(["--session", "lab-f1", "action", "dump-screen"])
show("zellij --session lab-f1 action dump-screen   "
     "(the session manager)", rc, out)
client.type("\x11", settle=1.0)
client.stop()
clean_slate()

# --- the web server -------------------------------------------------
rc, out = run(["web", "--daemonize"])
show("zellij web --daemonize", rc, out)
time.sleep(1.5)
rc, out = run(["web", "--status"])
show("zellij web --status", rc, out)
rc, out = run(["web", "--create-token"])
redacted = re.sub(r"[0-9a-f]{8}-[0-9a-f-]{27,}", "***", out)
show("zellij web --create-token   (token value redacted -- "
     "it is shown once, and the lab revoked it below)",
     rc, redacted)
curl = subprocess.run(
    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
     "http://127.0.0.1:8082/"], capture_output=True, text=True)
print(f"$ curl -s -o /dev/null -w '%{{http_code}}' "
      f"http://127.0.0.1:8082/\n{cur(curl)}\n")
page = subprocess.run(["curl", "-s", "http://127.0.0.1:8082/"],
                      capture_output=True, text=True).stdout
title = re.search(r"<title>([^<]*)</title>", page)
print(f"[the page's title: {title.group(1) if title else '?'}]\n")
rc, out = run(["web", "--revoke-all-tokens"])
show("zellij web --revoke-all-tokens", rc, out)
rc, out = run(["web", "--stop"])
show("zellij web --stop", rc, out)
time.sleep(1.0)
rc, out = run(["web", "--status"])
show("zellij web --status   (after stopping)", rc, out)
