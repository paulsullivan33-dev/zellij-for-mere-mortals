# The Neighbours

**Outcome: you can place Zellij against
the two multiplexers it succeeds — tmux
and GNU Screen — and say what each would
give you that Zellij doesn't, and what
you'd give up.**

This chapter is characterised, not
benchmarked: the lab ran Zellij, and
these neighbours are described from
their own documentation and long public
record. Both have their own guides in
this series, linked from the README —
and this chapter stays complete without
them.

## tmux

The incumbent. tmux (2007) runs on
practically every Unix, is small, starts
instantly, and is scriptable to the last
detail — its command language can build
and rearrange sessions from outside in
ways system administrators have relied
on for fifteen years. If you SSH into
strangers' servers, tmux is the
multiplexer that is probably already
there, and knowing it is a career skill,
not a tool preference.

Where Zellij pulls ahead is the first
hour. tmux shows you a status line and
waits for you to know that Ctrl b is the
prefix and that `%` splits vertically;
its discoverability is famously a
cheatsheet taped to a monitor. Zellij's
status bar teaches the current mode's
keys on screen, its layouts are a
purpose-built file format rather than a
command history replayed, and session
resurrection and the web client are
built in rather than plugins and
companions (tmux's own resurrection
story lives in external plugins).
Zellij also arrives with floating panes
and a mouse story that needs no setup.

Where tmux pulls ahead: ubiquity, a
tiny footprint next to Zellij's
52-megabyte binary, maturity — and your
existing muscle memory, which is a real
asset. Zellij even keeps a **tmux mode**
(Ctrl b prefix bindings) as a halfway
house for those fingers.

## GNU Screen

The elder. Screen (1987) invented this
category for most people: detach, log
out, log in, reattach — the core trick
of chapter 9 was already there when
terminals were hardware. It remains
installed by default on systems that
have changed little since, and its
detaching is bulletproof simplicity.

Against Zellij it reads as a tool from
before its users expected polish:
splitting exists but is spartan,
there's no comparable layout file
culture or plugin furniture, and
nothing on screen tells you what key
does what. People stay on Screen for
the same reason people stay on any
elder tool: it is there, it works, and
the job is rare and simple. For new
work on your own machine, Zellij is the
easier resident.

## The rest of the street

Two other answers to "one window is not
enough" deserve a sentence each. Your
**terminal emulator itself** may do tabs
and splits (many modern ones do, some
excellently) — that solves the window
pile but not the dropped-connection
problem, unless the emulator is itself
the session holder, which is precisely
the multiplexer's job. And **another
shell in another SSH session** solves
neither, which is why the multiplexer
category exists at all.

## The check

The decision is usually circumstantial,
and it is reversible: on *your* machine,
for work you return to, Zellij's
teaching interface and layout files pay
daily. On *other people's* servers,
use what's installed — and now you know
what you'd be missing, and what you
wouldn't.
