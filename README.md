# Zellij for Mere Mortals

A terminal window shows one program at a
time, and closing the window kills
whatever was running in it. **Zellij**
removes both limits. It is a **terminal
multiplexer**: one window holds many
**panes** and **tabs** of shells, and the
whole arrangement lives in a **session**
that keeps running when you close the
window, log out, or lose your connection —
you **attach** again later and everything
is where you left it.

Zellij is the modern entry in an old
family. Its selling points are that it
explains itself as you go — the status bar
at the bottom of the screen lists the keys
for the mode you are in — and that its
arrangements are written down in plain
text **layout** files you can share,
version, and start from. Sessions can
even be brought back after a crash, and
several people can attach to the same
session at once, one of them read-only if
you like.

One line to draw early, because later
chapters build on it: anyone who can
attach to your session sees everything in
it, including anything you type into a
pane. Treat the right to attach like the
right to use your shell — because that is
what it is.

This guide explains how Zellij's parts
fit together, walks a first session key by
key, and covers layouts, configuration,
crash recovery, plugins, and the built-in
web server. Every procedure was run for
real while the guide was written, and the
lab's transcripts are kept in the
repository as the evidence.

## What this guide covers

- [**What Zellij is**](what-zellij-is.md) —
  the mental model: a server holds your
  sessions, clients come and go, and
  nothing you run depends on a window
  staying open
- [**The moving parts**](the-moving-parts.md) —
  the server and the client, sessions,
  tabs and panes, plugins, and the layout
  and config files — and which part holds
  what
- [**Installing Zellij**](installing-zellij.md) —
  the official binary, the checksum check,
  and the version and setup checks that
  prove it runs
- [**Your first session**](your-first-session.md) —
  start, dismiss the welcome pane, run a
  command, split a pane, and quit — with
  a check at each step
- [**Layouts**](layouts.md) — arrangements
  written in KDL files: named tabs, panes
  that run a command, templates for the
  bars, and what a broken layout file
  tells you
- [**Panes and tabs**](panes-and-tabs.md) —
  splitting, moving, floating panes,
  fullscreen, tabs, and reading a live
  session's shape from outside it
- [**Modes and keys**](modes-and-keys.md) —
  the modal key system: one mode at a
  time, a status bar that lists its keys,
  scrollback and search, and the locked
  mode that hands every key to your
  program
- [**Configuring Zellij**](configuring-zellij.md) —
  the config file, themes, frame switches,
  your own keybindings — and the two ways
  a config file can be wrong, one loud
  and one silent
- [**Sessions: leaving, returning, and
  surviving a crash**](sessions.md) —
  detaching, attaching, killing on
  purpose, and resurrection after the
  server dies
- [**Plugins and the web
  server**](plugins-and-the-web.md) — the
  built-in plugins (the bars themselves
  are plugins), the session manager, and
  serving a session to a browser
- [**Recipes**](recipes.md) — a morning
  workbench layout, a long job you check
  on from a script, a guest watching
  read-only, and the habit that makes
  crashes boring
- [**The neighbours**](the-neighbours.md) —
  tmux and GNU Screen: what each does
  that Zellij doesn't, and vice versa
- [**Limits**](limits.md) — resurrection
  restores the arrangement, not your
  programs' memory; quitting is final;
  a misspelt option fails silently; and
  the other edges, named plainly
- [**Troubleshooting**](troubleshooting.md) —
  the keys that seem dead on first run,
  the layout command that needs a running
  session, the delete that argues back,
  and the traps this guide's lab fell
  into
- [**Glossary**](glossary.md) — the terms,
  collected in one place

## What it doesn't cover

Writing your own plugins. Plugins are
WebAssembly programs, usually written in
Rust, and building one is a programming
project with its own documentation; this
guide uses the built-in plugins and shows
where third-party ones would live.
Running Zellij as a shared public service
is likewise out — the web chapter covers
one person's server on their own machine,
with its login tokens, and chapter 13 is
honest about where the edges are.

## How to use this guide

Read chapter 1 for the model, and
chapter 2 before installing anything —
knowing which part holds what turns
later confusion into a named problem.
Chapters 3 and 4 get you a program and a
first session in the same sitting.
Chapter 5 is the one to read slowly even
if you are in a hurry: the layout file is
the feature you will reuse every day, and
its failure messages are the ones you
will meet again. The lab's transcripts
live in `zellij-lab/transcripts/`; its
driver and scenario scripts are in
`zellij-lab/` itself, and its sample
layout and config files are in
`zellij-lab/layouts/` and
`zellij-lab/configs/`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [tmux for Mere Mortals](https://paulsullivan33-dev.github.io/tmux-for-mere-mortals/)
- [GNU Screen for Mere Mortals](https://paulsullivan33-dev.github.io/gnu-screen-for-mere-mortals/)
- [SSH for Mere Mortals](https://paulsullivan33-dev.github.io/ssh-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/zellij-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/zellij-for-mere-mortals/blob/main/LICENSE-CODE).
