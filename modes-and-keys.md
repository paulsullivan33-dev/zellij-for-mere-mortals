# Modes and Keys

**Outcome: you understand Zellij's one
keyboard idea — modes — well enough to
predict what any key will do, find a key
you have forgotten from the status bar,
scroll and search a pane's history, and
hand every key to a full-screen program
with locked mode.**

## The idea

Zellij's keyboard is **modal**, like the
Vim editor's. Most of the time you are in
**Normal mode**, where keys go to the
program in the focused pane — your shell
gets what you type. A few keys in Normal
mode are Zellij's own: the mode keys.
Pressing one enters a **mode**, in which
the letter keys become commands — `n` no
longer types an "n", it makes a new pane.
Modes end by doing their job, or with
Enter or Esc, and you are back in Normal.

Twelve modes exist. You will live in six:

| Mode | Enter with | Its job |
|------|-----------|---------|
| Pane | Ctrl p | split, close, float, fullscreen panes |
| Tab | Ctrl t | open, close, rename, jump between tabs |
| Resize | Ctrl n | grow and shrink panes (h/j/k/l, arrows) |
| Move | Ctrl h | pick the focused pane up and move it |
| Scroll | Ctrl s | walk back through a pane's output |
| Session | Ctrl o | detach, and open the manager plugins |

The rest are specialists: **Locked**
(Ctrl g, below), **RenameTab** and
**RenamePane** (entered for you when you
ask to rename), **EnterSearch** and
**Search** (inside Scroll), and a **tmux**
mode that borrows tmux's Ctrl b prefix
habits for people whose fingers already
know them.

## The status bar is the manual

The design decision that makes modes
livable: the status bar at the bottom of
the screen re-draws itself for the mode
you are in, listing that mode's keys. In
Normal mode it shows the mode keys; in
Pane mode it shows the pane keys. You are
never expected to recall a key you can
read off the screen — the tables in
chapter 6 are for orientation, and this
bar is for the moment itself.

Some keys work in *every* mode, because
they are bound in the shared set: Ctrl g
(lock), Ctrl q (quit), Alt n (new pane),
Alt f (floating panes), Alt plus arrows
(focus), Alt i / Alt o (move a tab), and
Alt `[` / Alt `]` — which cycle the
**swap layouts**, Zellij's built-in
re-arrangements of the current tab's
panes (vertical, horizontal, stacked and
their variants, for when a split has
grown into a thicket).

The complete, exact list of default
bindings is not documentation trivia —
it is something the program itself will
print, and chapter 8 uses the same output
as the base you customise:

```bash
zellij setup --dump-config
```

Its `keybinds` section is the whole
keyboard, mode by mode, in the same KDL
as the config file.

## Scroll and search

A pane keeps its history. Enter **Scroll
mode** with Ctrl s:

| Key | What it does |
|-----|--------------|
| `j` / `k`, arrows | scroll down / up a line |
| Ctrl f / Ctrl b | a page down / up |
| `d` / `u` | half a page down / up |
| `s` | search: type a word, then `n` / `p` walk the matches (toggles: `c` case, `w` wrap, `o` whole word) |
| `e` | open the whole scrollback in your `$EDITOR` |
| `c` | copy the last command's output (in Search mode) |
| Ctrl c | jump back to the bottom, Normal mode |

The lab's evidence is plain: after
`seq 1 60`, the screen's tail showed
lines 32–60; two page-ups in Scroll mode
showed lines 1–29. The pane had held the
whole history all along — Scroll mode is
just the way to look at it.

`e` deserves a word. It writes the
scrollback to a temporary file and opens
your editor on it: the way to copy a long
error out of a pane, or save a transcript
of a session's work, without select-and-
paste gymnastics.

## Locked mode

Some programs want every key — a
full-screen editor, a game, another
multiplexer nested inside a pane (the
classic case: Zellij on your desk, tmux
on the server you attached to from a
pane, both fighting over Ctrl p). **Ctrl g**
enters **Locked mode**: Zellij stops
interpreting keys entirely and passes
everything to the pane, until Ctrl g
again unlocks.

The lab proved the pass-through rather
than describing it. Locked, it pressed
Ctrl p, `r` — the split keys. No split
happened; `list-panes` still showed one
terminal pane, and the pane's screen
showed the shell sitting at a prompt
reading `^Pr` — the control characters
had arrived at the *shell*, as literal
input, because in locked mode that is the
only place keys go. A typed command ran
normally. Unlocked, the same two keys
split the pane at once.

## The check

In any session: run `seq 1 60`, enter
Scroll mode (Ctrl s), page up twice with
Ctrl b, and confirm you are reading the
top of the output; Ctrl c returns you to
the prompt. Then Ctrl g, type `echo ok`,
watch it run, and Ctrl g again. You have
now used the two modes people find
strangest, on purpose.
