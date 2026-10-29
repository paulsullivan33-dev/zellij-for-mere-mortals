# Troubleshooting

**Outcome: the failures you are most
likely to meet — most of them in your
first week — each with the check that
separates it from the others.**

## "I type and nothing happens" (first run)

**Symptom:** a fresh session ignores
your shell commands; letters vanish.

**Cause:** the About / Release Notes
pane opened focused (chapter 4). Your
keys are going to a welcome screen.

**Check and fix:** look for the floating
pane and its footer, `<ESC> - Dismiss`.
Press Esc. To prevent it: set
`show_release_notes false` and
`show_startup_tips false` in the config
(chapter 8). To confirm which pane has
focus in general:
`zellij --session NAME action list-panes`
— the plugin panes are listed alongside
your terminals.

## "There is no active session!"

**Symptom:** a layout command fails with
exactly that.

**Cause:** `--layout` talks to a running
session (chapter 5). There isn't one
under that name — either it was never
started, or it was started under a
different name.

**Check:** `zellij list-sessions` shows
what exists. To *start* from a layout,
the flag is `--new-session-with-layout`.

## "My session vanished from the list"

Two different vanishings:

- **It was quit or killed.** Ctrl q, or
  `kill-session` — final by design
  (chapter 9). Nothing to recover; this
  entry is here so you stop looking.
- **It lists as EXITED.** The server
  died but the state was saved. Attach
  to resurrect it. If a *very young*
  session is missing entirely after a
  crash, its first save may not have
  happened yet — the `save-session`
  action (recipe 4) is the habit that
  prevents this one.

## "I changed the config and nothing changed"

**Symptom:** `--check` says "Well
defined.", the session ignores the
change.

**Cause, usually:** a misspelt option.
Unknown keys are ignored silently
(chapter 8) — the checker validates
syntax, not spelling.

**Check:** compare your line against
`zellij setup --dump-config` (the
defaults, spelled correctly). And if the
syntax itself were broken, the failure
would look different: the diagnostic
printed, and no session starts at all.
Two smaller causes: a session already
running was started under the old
config (start a new one to test), and a
second config directory (the checker
lists `/etc/zellij` after your home
one).

## "The layout loads, but the bars are gone"

**Cause:** your layout names panes but
no template (chapter 5). A layout gets
exactly what it asks for.

**Fix:** add the `default_tab_template`
with the tab-bar and status-bar plugin
panes, from chapter 5's example.

## "delete-session argues with me"

**Symptom:** deleting a running session
is refused, or `--force` prints
contradictory lines.

**Cause:** deletion of a live session
needs `--force` by design; its messages
are just untidy (chapter 9).

**Check:** ignore the prose, run
`zellij list-sessions`, and believe the
list.

## "My script's cleanup does nothing"

**Symptom:** `kill-all-sessions` in a
script errors or hangs the job.

**Cause:** without a terminal, the
confirmation prompt cannot be answered
and the command refuses (chapter 9).

**Fix:** pass `--yes` — and
`--force` for `delete-all-sessions` —
when the script's intent is certain.

## "Screen looks wrong inside a pane"

Colours off, keys doubled, a full-screen
program misbehaving: first suspect the
terminal you are running Zellij *in*
(limits chapter), second suspect nesting
— a multiplexer inside a pane wants
**Locked mode** (Ctrl g, chapter 7) so
the outer one stops eating its keys.
`zellij setup --check` and a fresh,
empty session (`zellij --session probe`)
separate "this session" from "this
installation" in one minute.

## The check

Every entry above ends in a command
whose output settles it. That is the
pattern to keep: in Zellij almost every
question has an outside view —
`list-sessions`, `list-panes`,
`dump-screen`, `setup --check` — so
debug from a second terminal, not from
inside the confusion.
