# Your First Session

**Outcome: a named session running, one
command executed in it, a second pane
beside the first, and a clean exit — with
a check at each step, including the trap
that catches almost every first-time
user.**

## Start it

```bash
zellij --session first
```

Naming the session is optional — without
`--session`, Zellij invents a name — but a
name you chose is a name you can find
again in chapter 9. The screen redraws:
a **tab bar** across the top, a large
pane with a shell prompt, and a **status
bar** along the bottom listing keys.

Check from a second terminal (or believe
this chapter and check later):

```bash
zellij list-sessions
```

```text
first [Created 3s ago]
```

## The first-run trap

On the very first run, a floating pane
opens in the middle of the screen: the
**About** pane, showing release notes.
It has the keyboard. Letters you type do
not reach your shell — they go to the
pane, which ignores most of them. It
feels exactly like a broken program.

It isn't. The pane's own footer says how
to leave:

```text
<ESC> - Dismiss
```

Press **Esc**. The pane closes, the
shell takes focus, and everything after
works as expected. (The pane is a plugin
doing a welcome job. Chapter 8 shows the
two config options — `show_release_notes`
and `show_startup_tips` — that stop it
appearing at all.)

How can you tell a pane has focus? Its
border is highlighted, and `list-panes`
names every pane in the session:

```bash
zellij --session first action list-panes
```

Before Esc, the lab's session showed an
`About Zellij` plugin pane; after Esc,
the terminal pane is the focused one.

## Run something, split something

Type a command, as in any shell:

```bash
echo hello-from-zellij
```

Now divide the window. Press **Ctrl p**
to enter **Pane mode** — watch the status
bar: it changes to list Pane mode's keys,
because the bar always shows the current
mode's menu. Then press **r**: a new pane
opens to the **right**, with its own
fresh shell. (Chapter 7 explains modes
properly; for now, borrow these two keys.)

Check the shape from outside:

```bash
zellij --session first action list-panes
```

```text
PANE_ID     TYPE      TITLE
plugin_0    plugin    (.) - zellij:link
terminal_0  terminal  Pane #1
terminal_1  terminal  Pane #2
```

Two terminal panes: the split is real,
and it is visible to any command that
asks the server — not just to your eyes.
That principle runs through this guide:
the server knows the session's shape, so
scripts can check it.

Move focus between the panes with
**Alt** and the arrow keys. Close the
new pane by focusing it and pressing
**Ctrl p** then **x**.

## Leave — two different ways

**Detach** (leave everything running,
walk away): press **Ctrl o** then **d**.
Your terminal returns to its normal
shell. The session is untouched;
`zellij list-sessions` still shows it,
and `zellij attach first` brings it back,
screen and all. The lab detached,
re-attached, and found the command it had
run — and its output — still on the
screen.

**Quit** (end the session): press
**Ctrl q**. The session and everything
in it are gone:

```bash
zellij list-sessions
```

```text
No active zellij sessions found.
```

Know which of the two you are pressing.
Detach is the everyday move; quit is a
full stop, for every client attached,
and there is no undo. Chapter 9 covers
the whole lifecycle, including what
happens when the ending isn't your idea.

## The check

You have a first session under control
when you can do this round trip without
looking anything up: start named, Esc
past the welcome, split with Ctrl p, r,
detach with Ctrl o, d, re-attach with
`zellij attach first`, and see your work
still there.
