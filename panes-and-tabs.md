# Panes and Tabs

**Outcome: you can shape a tab by hand —
split in either direction, move focus,
float a pane, go fullscreen, close what
you opened — open and rename tabs, and
prove each change happened by asking the
server.**

Chapter 4 borrowed two keys to split a
pane. This chapter is the full toolkit.
Every action here is done from **Pane
mode** (Ctrl p) or **Tab mode** (Ctrl t);
chapter 7 explains modes as a system.
The status bar lists each mode's keys
while you are in it, so the tables below
are a map, not a memory test.

## Splitting

In Pane mode:

| Key | What it does |
|-----|--------------|
| `n` | new pane (Zellij picks the direction with room) |
| `r` | split to the **right** |
| `d` | split **down** |
| `s` | new pane in a **stack** (see below) |

Outside any mode, **Alt n** opens a new
pane immediately — the split you will use
most. Each new pane runs a fresh shell in
the same working directory family as its
tab.

## Focus, fullscreen, frames

| Keys | What they do |
|------|--------------|
| Alt + arrows or Alt h/j/k/l | move focus between panes (at a tab's edge, moves to the next tab) |
| Pane mode, `h` `j` `k` `l` or arrows | move focus |
| Pane mode, `p` | cycle focus to the next pane |
| Pane mode, `f` | pane **fullscreen** — fills the tab until toggled back |
| Pane mode, `z` | toggle the drawn **frames** around panes |
| Alt `=` / Alt `-` | grow / shrink the focused pane |

A **stack** is a column of panes sharing
one slot: only one is expanded at a time,
the others show as title strips. It suits
a set of logs you check one at a time.

## Floating panes

| Keys | What they do |
|------|--------------|
| Alt f | show or hide the floating panes |
| Pane mode, `w` | make the focused pane float |
| Pane mode, `e` | toggle a pane between floating and embedded (tiled) |

Floating panes sit above the tiling —
the About pane of chapter 4 was one — and
can be dragged and resized with the
mouse, as can tiled pane borders. Mouse
support is on by default; chapter 8 has
the switch to turn it off.

## Closing and renaming panes

Pane mode: `x` closes the focused pane
(its program gets the usual hangup a
closed terminal sends; a shell simply
exits). `c` starts renaming the pane —
type the name, press Enter. A pane's name
is what `list-panes` shows as its title
when no program has set one.

## Tabs

In Tab mode (Ctrl t):

| Key | What it does |
|-----|--------------|
| `n` | new tab |
| `x` | close the tab (and every pane in it) |
| `r` | rename the tab — type, Enter |
| `1`–`9` | jump to a tab by position |
| `h` / `l`, arrows, Tab | previous / next / last tab |
| `s` | **sync** the tab: keystrokes go to all its panes at once |
| `b` | break the focused pane out into its own tab |

## The check — ask the server

Nothing in this chapter needs to be taken
on faith, because the server answers
questions about the session from any
other terminal:

```bash
zellij --session work action list-panes
zellij --session work action list-tabs
zellij --session work action list-clients
```

The lab split a pane with Ctrl p, `r`
and found two terminal panes listed;
renamed the second tab to `Second` and
read the name back with
`action query-tab-names`. One pane's
screen, by id, is:

```bash
zellij --session work action dump-screen --pane-id terminal_1
```

Two more verbs round out the picture.
`action dump-layout` prints the session's
whole arrangement as a layout file
(chapter 5's round trip). And actions run
from *inside* a session need no session
name at all — a pane's shell already
knows where it lives:

```bash
zellij action new-pane --direction down -- sh -c 'echo inner-pane; sleep 300'
```

typed at a prompt inside the session,
opens a pane beneath you running that
command. The lab ran it and then read the
new pane's screen from outside:
`inner-pane`. Scripts that live inside a
session — build scripts that open a log
pane, test scripts that arrange their own
observers — are built from this one
trick.
