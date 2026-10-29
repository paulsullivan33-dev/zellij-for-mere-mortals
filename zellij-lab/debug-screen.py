#!/usr/bin/env python3
"""Debug: what does the client actually paint?"""
import re
import sys
import time

from drive import Client, run, wait_session

NAME = "lab-debug"
run(["delete-all-sessions"])
client = Client(["--session", NAME])
wait_session(NAME)
client.pump(3.0)

raw = bytes(client.output)
# Crude ANSI strip: drop escape sequences, keep text and newlines.
text = re.sub(rb"\x1b\[[0-9;?]*[A-Za-z]", b"", raw)
text = re.sub(rb"\x1b\][^\x07\x1b]*(\x07|\x1b\\)", b"", text)
text = re.sub(rb"\x1b[()][0-9A-B]", b"", text)
print("=== client output, escapes stripped (last 3000 chars) ===")
print(text.decode("utf-8", "replace")[-3000:])
print("=== end ===")

rc, out = run(["--session", NAME, "action", "list-panes"])
print(rc, out)
rc, out = run(["--session", NAME, "action", "dump-screen"])
print("dump-screen rc", rc, "out:", repr(out))
client.stop()
run(["delete-all-sessions"])
