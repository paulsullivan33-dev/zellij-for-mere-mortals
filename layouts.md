# Layouts

**Outcome: you can write a layout file
that opens your usual tabs and panes —
one of them already running a command —
start a session from it, and read the
error when the file is wrong.**

## Why layouts are the feature

Everything in chapter 4 can be done by
hand, every time: split, open tab, split
again, start the log tail. A **layout**
writes that arrangement down once, in a
text file, and Zellij rebuilds it on
demand — for you, for a teammate who
shares the file, or for a script. It is
the difference between a desk you tidy
every morning and a desk that is simply
tidy.

Layouts are written in **KDL**, a plain
document format of nested named blocks.
You do not need to learn KDL in general;
the shapes below cover most of what a
layout ever says.

## A first layout

The lab's working example,
`zellij-lab/layouts/workbench.kdl`:

```kdl
layout {
    tab name="Main" {
        pane
    }
    tab name="Pair" {
        pane split_direction="vertical" {
            pane
            pane
        }
    }
    tab name="Worker" {
        pane command="sh" {
            args "-c" "echo worker-started; sleep 3600"
        }
    }
}
```

Read it as a description of the finished
thing: three tabs. `Main` holds one pane
(a shell). `Pair` holds two panes side by
side (`split_direction="vertical"` divides
left from right). `Worker` holds one pane
that does not open a shell at all — it
runs the given command, here a stand-in
that prints a line and then sleeps, the
way a build, a server, or a log tail
would stay running.

Start a session from it. A *new* session
takes its layout with a flag whose name
says exactly that:

```bash
zellij --session work --new-session-with-layout workbench.kdl
```

## The check — from outside

The arrangement is checkable without
looking at the screen:

```bash
zellij --session work action list-tabs
```

```text
TAB_ID  POSITION  NAME
0       0         Main
1       1         Pair
2       2         Worker
```

And the Worker pane really ran its
command — its screen contains the line it
printed:

```bash
zellij --session work action dump-screen
```

(with the Worker tab focused) shows
`worker-started`. In `list-panes`, the
Worker pane's title is the command line
itself.

## The bars are the layout's business

Look again at the session the file above
creates — something is missing. There is
no tab bar and no status bar. A layout
that names panes gets exactly the panes
it names; the familiar furniture comes
from the *default layout*, not from the
air.

To give every tab the bars, a layout adds
a **template** — a block saying what each
tab is wrapped in:

```kdl
layout {
    default_tab_template {
        pane size=1 borderless=true {
            plugin location="zellij:tab-bar"
        }
        children
        pane size=1 borderless=true {
            plugin location="zellij:status-bar"
        }
    }
    tab name="Main" {
        pane
    }
}
```

`children` is where each tab's own panes
go. The two one-line borderless panes run
the tab-bar and status-bar plugins
(chapter 2: the furniture is plugins).
The lab ran the same workbench both ways
and compared `action dump-layout` output:
without the template, each tab is a bare
pane; with it, each tab carries the two
bar panes. (The full with-bars file is
`zellij-lab/layouts/workbench-with-bars.kdl`.)

## Adding to a running session

`--layout` without "new session" means
something different, and meeting the
difference once is how everyone learns
it: together with `--session`, it **adds**
the file's tabs to the session already
running under that name.

```bash
zellij --session work --layout extra-tab.kdl
```

The lab's `extra-tab.kdl` is one tab; the
session's tab list gained it, going from
three tabs to four. And if no session of
that name is running, the same command
fails with `There is no active session!`
— the flag is an instruction to a live
server, not a way to start one.

## Layouts by name, and layouts you have

A layout file placed in
`~/.config/zellij/layouts/` can be used
by name alone, from anywhere:

```bash
zellij --session work --new-session-with-layout workbench
```

The built-in layouts answer to names the
same way: `default`, `classic`, `compact`,
`disable-status-bar`, and `strider` (a
file-browser layout built around a plugin
of the same name). Print any of them to
see how it is put together:

```bash
zellij setup --dump-layout compact
```

One honest wart from the lab: dump an
unknown name and Zellij prints nothing at
all and exits successfully. Silence here
means "no such layout", not "empty
layout".

## Saving the arrangement you have

A session you have arranged by hand can
be written back out as a layout:

```bash
zellij --session work action dump-layout > my-layout.kdl
```

The lab did exactly this round trip —
dumped a running three-tab session to a
file, started a fresh session from the
file, and got the same three tabs back.
The dump is complete and verbose (it
includes the swap layouts of chapter 6),
so treat it as a starting point to trim,
not as handwriting.

## When the file is wrong

KDL is strict, and a broken layout fails
at the door, with the best error messages
in the program. The lab's `broken.kdl` is
missing a closing brace; the client
prints this and opens on the error — no
session is created:

```text
  × Failed to parse Zellij configuration
   ╭─[.../layouts/broken.kdl:1:8]
 1 │ ╭─▶ layout {
 2 │ │       tab name="Oops" {
 3 │ │           pane split_direction="vertical" {
 4 │ │               pane
 5 │ │       }
 6 │ ├─▶ }
   · ╰──── Kdl Deserialization Error
   ╰────
  help: For more information, please see our configuration guide: https://zellij.dev/documentation/configuration.html
```

The file, the lines, and the shape of the
mistake are all in the message. Fix the
file and start again; nothing is left
half-built behind you.
