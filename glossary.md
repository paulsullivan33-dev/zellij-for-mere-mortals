# Glossary

**Action** — a command sent to a running
session, from the keyboard or from
`zellij action …` in a shell: new-pane,
dump-screen, save-session, and dozens
more.

**Attach** — connect a client to an
existing session and work in it.
`zellij attach NAME`; `--create` starts
the session if it is missing,
`--create-background` starts it without
attaching.

**Client** — the part of Zellij that
draws on your terminal and forwards your
keys. Many clients can attach to one
session; closing a client harms nothing.

**Config file** — `~/.config/zellij/
config.kdl`: your standing options,
theme, and keybindings, in KDL.

**Detach** — leave a session without
ending it: Ctrl o, then d. The server
keeps everything running.

**EXITED session** — a session whose
server has died but whose saved state
remains; listed by `list-sessions` with
"(EXITED - attach to resurrect)".

**Floating pane** — a pane that hovers
above the tiled panes instead of sharing
their grid. Alt f shows or hides them.

**KDL** — the document format of layout
and config files: nested named blocks in
plain text.

**Layout** — a KDL file describing tabs,
panes, and the commands they run, so a
session can be rebuilt on demand. Also
**swap layouts**: built-in rearrangements
of a live tab, cycled with Alt [ and ].

**Mode** — a state of the keyboard in
which letter keys are commands rather
than text: Normal, Pane, Tab, Resize,
Move, Scroll, Session, Locked, and
others.

**Pane** — one rectangle in a tab, running
one program: a shell, a command, or a
plugin.

**Plugin** — a pane whose program is a
WebAssembly module. The tab bar, status
bar, session manager and About pane are
built-in plugins; `zellij list-aliases`
names them.

**Resurrection** — rebuilding an EXITED
session from its saved layout and
metadata. Restores the arrangement, not
the programs' state.

**Server** — the background process, one
per session, that holds the session's
tabs, panes, programs, and scrollback.

**Session** — one whole workspace: a set
of tabs held by a server, surviving its
clients.

**Session serialization** — the server's
ongoing saving of a session's layout and
metadata under
`~/.cache/zellij/contract_version_1/
session_info/`, which makes resurrection
possible. The `save-session` action
forces a save now.

**Status bar** — the bottom line of the
screen: a plugin that lists the current
mode's keys.

**Tab** — one full-window page of a
session, holding panes.

**Tab bar** — the top line listing tabs;
also a plugin.

**Watch** — attach read-only:
`zellij watch NAME`. Keys pressed by a
watcher never reach the session.
