# Sessions: Leaving, Returning, and Surviving a Crash

**Outcome: you can leave a session three
ways and know exactly what each does,
return to it, end it on purpose, and —
the part no other multiplexer guide in
this series can offer — bring it back
after its server has been killed, with a
clear account of what resurrection does
and doesn't restore.**

## Leaving without ending: detach

Detach: **Ctrl o**, then **d** (Session
mode's first key). The client closes;
the server and everything in it keep
running. This is the normal way to end a
workday, close a laptop, or drop off a
flaky network on purpose.

Return with:

```bash
zellij attach work
```

or start a session only if none exists:

```bash
zellij attach work --create
```

and create one *without* attaching — the
scripting form, which chapter 11 uses:

```bash
zellij attach work --create-background
```

The lab's round trip: run a command,
detach, re-attach, and the command's
output is still on the pane's screen.
Nothing paused while nobody was looking.

## Ending on purpose: quit and kill

**Ctrl q** quits: the session ends for
every attached client, immediately. From
outside, the same ending by name:

```bash
zellij kill-session work
```

A killed session is *gone* — not parked,
not listed, not resurrectable. The lab
killed a session and `list-sessions`
answered `No active zellij sessions
found.` Killing is the right ending for
work that is finished; it is simply not
a pause button. (Deleting a session's
saved state is a separate verb,
`delete-session`, used below.)

## Ending by accident: the crash

Suppose the server process dies — a
machine reboot, an over-zealous cleanup,
a kill signal. Zellij writes each
session's state to disk as it runs
(exactly where is below), and a session
whose server died is not deleted. It
changes state:

```text
$ zellij list-sessions
lab-crash [Created 6s ago] (EXITED - attach to resurrect)
```

`EXITED` is an invitation. Attach, and
the session is rebuilt from its saved
state:

```bash
zellij attach lab-crash
```

The lab did this the hard way: built a
session with a second pane and a tab
renamed `Keepsake`, killed the server
process with SIGKILL — no cleanup, no
warning — and attached to the EXITED
entry. The result:

```text
$ zellij --session lab-crash action list-tabs
TAB_ID  POSITION  NAME
0       0         Keepsake
```

Both panes came back too. What
resurrection restores is the
**arrangement**: tabs, their names, the
pane layout, working directories — and
what it does not restore is the
**contents**. Each pane is a fresh shell
at its prompt. The long build that was
running is not resumed; its scrollback
is not part of the saved state by
default. (An option, `serialize_pane_
viewport`, can add the visible screen —
off by default, and process state itself
is beyond any multiplexer.)

## What makes it possible

The saved state lives, per session, at:

```text
~/.cache/zellij/contract_version_1/session_info/<name>/
    session-layout.kdl
    session-metadata.kdl
```

The layout file is literally a layout in
chapter 5's sense — the lab's began:

```kdl
layout {
    cwd "/home/hatch/workspace/zellij-for-mere-mortals/zellij-lab"
    tab name="Keepsake" focus=true hide_floating_panes=true {
```

so resurrection is not magic: it is a
layout, written continuously by the
server, plus metadata about focus and
geometry. The state is updated on an
interval, which has one practical
consequence the lab hit: a *brand new*
session, killed within its first seconds,
may not have been saved yet. The force
save is an action:

```bash
zellij --session work action save-session
```

Run it after arranging anything you would
miss. Two standing options govern all of
this, from chapter 8's territory:
`session_serialization` (on by default)
turns saving off, and
`resurrection_disabled` disables it
outright on machines where saved sessions
are not wanted.

## Tidying up

EXITED sessions linger in the list until
you delete them:

```bash
zellij delete-session lab-crash
```

For a session that is still *running*,
delete refuses — `exists and is active,
use --force` — and `--force` kills and
deletes it in one step. One honest wart:
the forced delete's messages can confuse
(the lab saw a success line and a
"not found" line from the same command).
Judge a deletion by `list-sessions`
afterwards, never by the message.

The wholesale versions,
`kill-all-sessions` and
`delete-all-sessions`, ask for
confirmation. Unattended — in a script,
with no terminal — they will not proceed
at all; pass `--yes` (and `--force` for
delete) when the script really means it.
The lab's scenarios all begin that way.

## Several people, one session

Any number of clients can attach to one
session; they share the same panes, and
one person's typing is everyone's screen.
For showing without sharing the keyboard,
attach read-only:

```bash
zellij watch work
```

The lab attached a watcher, had it type
a command line, and dumped the pane's
screen from outside: the watcher's line
was nowhere on it — only the real
client's command had run. That is the
safe way to let someone look over your
shoulder, and chapter 1's caution is the
other side of it: a normal attachment is
a full set of hands, not a window.

## The check

Arrange a session you can recognise —
two panes, a renamed tab — then:

```bash
zellij --session work action save-session
zellij list-sessions
```

Kill nothing yet; first detach and
re-attach until that is boring. When you
have a session you truly don't need, run
the whole ending: kill its server
process (`pgrep -af zellij` shows the
server's command line, with the session
name at the end), watch it list as
EXITED, attach, and meet your arrangement
again — with fresh shells in it.
