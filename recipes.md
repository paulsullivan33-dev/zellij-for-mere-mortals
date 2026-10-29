# Recipes

**Outcome: six small jobs done with the
parts from earlier chapters — each one
something the lab actually ran.**

## 1. The morning workbench

Keep a layout in the layout directory
(chapter 5) — the lab's is
`workbench-with-bars.kdl`, three tabs,
one of them a worker pane — and install
it once:

```bash
mkdir -p ~/.config/zellij/layouts
cp workbench-with-bars.kdl ~/.config/zellij/layouts/workbench.kdl
```

Every morning after:

```bash
zellij --session work --new-session-with-layout workbench
```

Same tabs, same split, worker already
working. Check the shape from any other
terminal before you even sit down:

```bash
zellij --session work action list-tabs
```

## 2. The long job you leave behind

Start the session without attaching, and
let it run unwatched:

```bash
zellij attach nightly --create-background
```

Give the job its own pane in that
session — from a layout (recipe 1's
Worker tab is this pattern) or by
attaching once to set it going. Then
checking on it, from a script or a
phone-tunnelled shell, never needs you
to attach and disturb it:

```bash
zellij list-sessions
zellij --session nightly action dump-screen
```

`dump-screen` prints what the focused
pane shows; `--pane-id` names another
(chapter 6). A script can grep that
output for `FAILED` or a progress line
and say nothing at all while the job is
healthy — silence as the success signal.

## 3. Show someone, without handing over

A colleague needs to see the session,
not drive it:

```bash
zellij watch work
```

on their terminal attaches read-only:
their keys never reach the panes
(chapter 9 proved it — the watcher's
typed command never appeared). To
collaborate for real, they attach
normally — knowing chapter 1's rule,
that an attached client is a full set
of hands.

## 4. The crash habit

Resurrection reads state the server
saves as it goes — but a fresh session
may not have been saved yet (chapter 9).
After arranging anything precious, spend
the one command:

```bash
zellij --session work action save-session
```

Then a dead server is a drill, not a
disaster: `zellij list-sessions` shows
the session `(EXITED - attach to
resurrect)`, and `zellij attach work`
rebuilds the arrangement. Afterwards,
tidy the list of sessions you will never
resurrect:

```bash
zellij delete-session old-experiment
```

and judge the deletion by the listing,
not the message.

## 5. Rename from outside

A session can be renamed without
attaching — useful when a script created
one under a working title and the day
gave it a better one:

```bash
zellij --session work action rename-session migration
```

The lab renamed a live session this way
and watched `list-sessions` follow. (Tab
renaming from outside exists too; the
lab found it less reliable than renaming
with Ctrl t, `r` from inside, which is
the way chapter 6 teaches.)

## 6. A script that tidies up after itself

Automation that creates sessions should
also end them. Two rules from chapter 9:
killing is final, and unattended kills
need their `--yes`:

```bash
zellij kill-session scratch
zellij delete-all-sessions --yes --force
```

The second line is the lab's own
reset button — every scenario begins by
deleting whatever an earlier run left,
so the transcripts you have been reading
started from an empty list every time.
