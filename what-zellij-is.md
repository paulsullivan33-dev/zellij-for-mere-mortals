# What Zellij Is

**Outcome: you can say what a terminal
multiplexer is, what problem it solves
twice over, and why Zellij's version of
it explains itself while you use it.**

## Two problems, one tool

Open a terminal and start a long job — a
big download, a slow build, an editor
with three files open. Two things are
true and both are annoying:

1. The window shows one thing. To watch a
   log while the build runs, you open a
   second window, and a third, and soon
   the desktop is a pile of rectangles
   you are arranging by hand.
2. The job's life is tied to the window.
   Close the window, drop the network
   connection, or let the laptop sleep
   at the wrong moment, and the job
   dies with it.

A **terminal multiplexer** solves both.
It sits between you and your shells. On
the screen side, it divides one window
into **panes** (rectangles, each running
its own program) grouped into **tabs**.
On the life side, it moves your shells
into a **session** held by a background
**server**, so the shells — and
everything running in them — survive the
window.

That second half is the deeper one. With
a multiplexer, "my connection dropped" is
a shrug: reconnect, attach to the
session, and the build is still building,
the editor still has your files open, the
scrollback still shows what happened
while you were gone.

## Where Zellij fits

Multiplexers are old. GNU Screen dates
from the 1980s; tmux, from 2007, is the
one most servers already have. Zellij is
the newer entry (first released in 2021,
written in Rust, and the version this
guide's lab ran is 0.45.1). It keeps the
family model — server, sessions, panes —
and changes the experience around it:

- **It teaches as you go.** A status bar
  along the bottom lists the keys that
  work *right now*, for the mode you are
  in. You rarely need to memorise a key
  before you need it.
- **Arrangements are files.** A layout —
  which tabs, which panes, which command
  in each — is a short text file in a
  format called KDL. Write it once, start
  from it every day, share it with a
  team.
- **Sessions can come back from the
  dead.** If the server process is
  killed, the session's saved state lets
  you attach and get the arrangement
  back (chapter 9 shows exactly what
  does and doesn't survive).
- **The interface is partly plugins.**
  The tab bar and status bar are
  WebAssembly plugins, and other people
  can write more.
- **It can serve a session to a
  browser.** Version 0.45 has a built-in
  web server, covered in chapter 10.

## The one caution

A session is shared by attaching. Anyone
who can attach to your session — a second
client on the machine, a guest you invite
to watch, a browser holding a login token
for the web server — sees every pane,
including a pane where you are typing a
password. That is the tool working as
designed. The chapters on sessions and on
the web server come back to this, because
the convenience and the exposure are the
same feature.

## The check

On any machine with Zellij installed:

```bash
zellij --version
```

```text
zellij 0.45.1
```

That one line is the version this whole
guide was verified against. (Install
first if you need to — chapter 3.)
