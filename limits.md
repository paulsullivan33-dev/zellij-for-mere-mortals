# Limits

**Outcome: you know where Zellij's
promises stop — in its own words where
possible, and in the lab's where the lab
found the edge first.**

- **Resurrection restores arrangement,
  not state.** Tabs, names, splits and
  working directories come back after a
  crash. The program that was running in
  a pane does not resume, and its output
  history is not saved by default.
  Anything that cannot survive being
  restarted — an editor with unsaved
  changes is the standing example — is
  not protected by a multiplexer.
- **Quitting and killing are final.**
  Ctrl q and `kill-session` end a session
  outright; there is no trash can and no
  resurrection for a session ended on
  purpose. The saved state that makes
  crash recovery possible belongs to the
  crash case only.
- **A config typo fails silently.** An
  option name Zellij doesn't recognise
  is ignored — no warning, "Well
  defined." from the checker — so the
  only proof a config change worked is
  seeing it work (chapter 8). Syntax
  errors, by contrast, are loud and
  total: no session starts.
- **Some silences mean "not found".**
  `zellij setup --dump-layout` of an
  unknown name prints nothing and exits
  0. A script that dumps layouts must
  check the output is non-empty, not
  just the exit code.
- **`--layout` is not `--new-session-
  with-layout`.** One adds tabs to a
  running session and errors if there
  isn't one; the other starts a session.
  The two flags' confusion is this
  guide's most-repeated trap, and it is
  a naming problem in the tool, not in
  you.
- **Deletion messages can mislead.**
  A forced `delete-session` printed a
  success and a "not found" in the same
  breath in the lab. Verify by listing.
  Similarly, the wholesale kill/delete
  commands refuse to run without a
  terminal unless told `--yes` — in
  automation, that refusal surfaces as
  an error, not a question.
- **Sharing is all-or-nothing per
  client.** An attached client can type
  everywhere; a watcher can type
  nowhere. There is no per-pane
  permission and no way to let a guest
  drive one pane while you keep another.
  The web server adds login tokens, but
  a token is a bearer credential: whoever
  holds it, holds it.
- **It is not a terminal emulator.**
  Zellij runs *inside* one — it draws
  with the terminal's capabilities, so
  fonts, true colour, and image support
  are your terminal's business, and
  Zellij needs a Unix terminal (on
  Windows, that means WSL).
- **The binary is heavyweight.** One
  static file of 52 MB, plus a server
  process per session. On a small or old
  machine where tmux is already present,
  that weight is a fair argument.
- **The web client is young.** Server,
  tokens and opt-ins are verified in
  chapter 10; the in-browser experience
  is new in 0.45, and this guide files
  its use as documented-only rather
  than pretend otherwise.

## The check

Read the first limit again the next time
you are tempted to treat a session as a
save file: a multiplexer protects your
*arrangement* and your *access*, never
your unsaved work. Save files in editors;
let Zellij keep the desk.
