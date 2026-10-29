# The Moving Parts

**Outcome: given any Zellij behaviour,
you can name which part produced it —
the server, the client, a plugin, or a
file — and know where that part's state
lives.**

Six parts do all the work.

## The server

One background process per session,
holding the session's real state: the
tabs, the panes, the programs running in
them, and their scrollback. When you run
`zellij` and no server exists for your
session yet, one starts. The server is
why closing your terminal window changes
nothing: the window was never where your
work lived.

You can see the servers as ordinary
processes — the lab listed them while
testing crash recovery:

```text
zellij --server /tmp/zellij-0/contract_version_1/lab-crash
```

(that is the process's own command line,
found with `pgrep`). Kill that process
and you have killed the session's present
tense — chapter 9 is about what remains.

## The client

The client is the part that touches your
terminal: it draws the panes and forwards
your keystrokes to the server. Running
`zellij` starts a client (and a server,
if needed). Several clients can attach to
one session at once, and each sees the
same panes. A client that can only watch
is started with `zellij watch`.

Closing a client is harmless. Quitting
from inside — Ctrl q — is not: it ends
the session for everyone. Chapter 9 draws
that line carefully.

## Sessions, tabs, panes

The nouns, in nesting order:

- A **session** is one whole workspace,
  with a name (`work`, or the random name
  Zellij invents if you don't give one).
- A session holds **tabs**. Each tab
  fills the window.
- A tab holds **panes**: rectangles, each
  running one program — usually a shell.
  Panes tile side by side, or float above
  the tiles.

Every session also holds a few panes you
didn't open: plugin panes (next section)
and one hidden helper. `list-panes` shows
the cast for a fresh session:

```text
PANE_ID     TYPE    TITLE
plugin_0    plugin  (.) - zellij:link
plugin_3    plugin  About Zellij
terminal_0  terminal  Pane #1
```

## Plugins

A **plugin** is a pane whose program is a
WebAssembly module instead of a shell.
The parts of Zellij that feel like
furniture are plugins: the **tab bar**
across the top, the **status bar** along
the bottom with its key hints, the
**session manager**, the file picker, the
About pane that greets you on first run.
The built-in set answers to short names
("aliases") — the lab listed them:

```text
about
compact-bar
configuration
filepicker
plugin-manager
session-manager
status-bar
strider
tab-bar
welcome-screen
```

Because plugins are just panes with a
different kind of program inside, they
open, close, and take focus like any
pane. That is also why the About pane can
steal your first keystrokes: on a first
run it opens *focused*. Chapter 4 deals
with it.

## The layout file

A **layout** is a KDL text file saying
which tabs and panes a session starts
with, and which command each pane runs.
Layouts are how an arrangement stops
being something you rebuild by hand every
morning. Built-in layouts (default,
classic, compact, and two more) cover the
common shapes; your own live in
`~/.config/zellij/layouts/` or anywhere
you pass a path. Chapter 5.

## The config file

One file, `~/.config/zellij/config.kdl`,
holds your standing choices: theme,
whether panes get drawn frames, your
extra keybindings, and options like
turning off the first-run panes. It uses
the same KDL format as layouts. Chapter 8
covers it, including its strangest
property: half its mistakes are silent.

## Where the state lives

`zellij setup --check` prints the three
directories that matter:

- **Config:** `~/.config/zellij` — your
  config and your layouts.
- **Data:** `~/.local/share/zellij` —
  downloaded plugins live here.
- **Cache:** `~/.cache/zellij` — including
  the saved state of sessions, under
  `contract_version_1/session_info/`,
  one folder per session holding a
  `session-layout.kdl` and a
  `session-metadata.kdl`. Chapter 9 opens
  those files.

## The check

```bash
zellij setup --check
```

It reports each directory and, once you
have a config file, whether that file is
well formed. Run it now so the paths
above are your machine's paths, not this
guide's.
