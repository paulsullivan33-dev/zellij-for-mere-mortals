# Configuring Zellij

**Outcome: your choices live in a config
file Zellij reads at start — a theme,
frames off, the welcome panes silenced,
one key of your own — and you know how to
tell a config that is working from the
two kinds that are not.**

## The file

Configuration is one KDL file:

```text
~/.config/zellij/config.kdl
```

There is no settings screen and no
registry; the file is the whole story,
and `zellij setup --dump-config` prints
the *default* config in full — several
hundred lines, mostly the default
keybindings — which is the honest way to
see every option's name and factory
setting before you change one.

## A small, real config

The lab's working config,
`zellij-lab/configs/good.kdl`:

```kdl
theme "nord"
pane_frames false
show_release_notes false
show_startup_tips false

keybinds {
    normal {
        bind "Alt w" { CloseFocus; }
    }
}
```

Line by line:

- `theme "nord"` picks one of the
  built-in colour themes.
- `pane_frames false` turns off the drawn
  borders around panes (chapter 6's `z`
  key toggles them per session; this sets
  the standing choice).
- `show_release_notes false` and
  `show_startup_tips false` silence
  chapter 4's first-run panes.
- The `keybinds` block **adds** one
  binding: in Normal mode, Alt w closes
  the focused pane. It adds — it does not
  replace. Unless a keybinds block says
  `clear-defaults=true`, your bindings
  are merged over the defaults, so one
  small block cannot accidentally unbind
  the keyboard.

## The check — before any session

```bash
cp zellij-lab/configs/good.kdl ~/.config/zellij/config.kdl
zellij setup --check
```

```text
[CONFIG FILE]: Well defined.
```

That line is the config file's health
certificate, and it is the first of two
ways to be wrong. Then start a session
and confirm the file is not just valid
but *in force*: no About pane appears
(the two `show_` lines did that), panes
have no frames, and Alt w — your key —
closes a pane. The lab did all three, and
used Alt w to close the pane it had just
opened with Alt n.

## Wrong, loudly

Break the file's syntax — the lab's
`syntax-error.kdl` drops a brace — and
the failure is total and informative:

```bash
zellij setup --check
```

prints the same style of diagnostic as
chapter 5's broken layout: file, line
span, the shape of the mistake. Starting
a session with that config prints the
diagnostic and creates no session. A
loud failure at the door is a kindness:
you fix the file, not the session.

## Wrong, silently

The other failure has no message at all.
An option Zellij does not recognise is
simply ignored. The lab added a line
inventing an option:

```kdl
banana_mode true
```

`setup --check` still answered
"Well defined.", and the session started
normally, with no banana mode anywhere.
A misspelt real option fails exactly the
same way — silently, by doing nothing.

So the working rule is: a config change
is not done when `--check` passes. It is
done when you have seen the change in a
session — the frames gone, the key
working, the welcome pane absent. The
check button in this chapter's config is
Alt w: if it closes a pane, the file was
read; if it types nothing and nothing
happens, suspect a typo before anything
else.

## Options worth knowing

From `zellij options --help` and the
default config (the lab read both in
full; a few to start from):

- `default_layout "compact"` — start
  sessions from a layout other than
  `default`.
- `default_mode "locked"` — start with
  the keyboard already handed to your
  programs.
- `mouse_mode false` — turn mouse support
  off entirely.
- `copy_on_select false` — by default,
  selecting text with the mouse copies
  it; this stops that.
- `session_serialization false` — turn off
  the saved state chapter 9's
  resurrection depends on.
- `scrollback_editor` — the editor Scroll
  mode's `e` key opens, if you don't want
  `$EDITOR`.

Almost every option also exists as a
one-session command-line override under
`zellij options …` — the help text is
long because the surface is honest about
being large. The config file remains the
place for choices you mean to keep.
