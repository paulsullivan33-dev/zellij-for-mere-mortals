# Installing Zellij

**Outcome: Zellij is on your machine from
an official source, the download's
checksum matches the project's, and two
checks — version and setup — prove the
program runs.**

## What you are installing

One program. The official release ships
it as a single static binary: no runtime,
no dependencies, nothing else to install
alongside it. The lab's copy is
52,547,536 bytes — largish for a terminal
tool, and the size has a reason: the
plugins are inside. Chapter 2's tab bar
and friends are WebAssembly modules
bundled with the program, about 1.5 MB
each when written out; chapter 10 lists
them.

## The download

Releases live on the project's GitHub
page. For a 64-bit Linux machine, the
asset is named
`zellij-x86_64-unknown-linux-musl.tar.gz`
(about 18 MB — the binary is compressed
for travel). Download the archive **and**
the release's checksum file, then check
one against the other before you trust
the program:

```bash
sha256sum zellij
```

Compare the answer, character for
character, with the line for the plain
`zellij` binary in the checksum file
(the checksums are published per binary,
not per archive). The lab did this for
0.45.1 and the sums matched; the checksum
step is cheap and it is the difference
between "a zellij" and *the* zellij.

Unpack and put the binary somewhere on
your `PATH`:

```bash
tar xzf zellij-x86_64-unknown-linux-musl.tar.gz
mkdir -p ~/.local/bin
cp zellij ~/.local/bin/
```

Other routes exist — most Linux package
managers carry Zellij, macOS users can
use Homebrew, and `cargo install zellij`
builds it from source. They all install
the same program; this guide's checks
work the same whichever route you took.
On Windows, Zellij runs inside WSL — it
needs a Unix terminal to multiplex.

## The checks

Version first:

```bash
zellij --version
```

```text
zellij 0.45.1
```

Then ask Zellij to inspect its own setup:

```bash
zellij setup --check
```

On a machine that has never run it, the
lab's answer began:

```text
[Version]: "0.45.1"
[CONFIG DIR]: Not Found
 On your system zellij looks in the following config directories by default:
 "/home/hatch/.config/zellij"
 "/etc/zellij"
[CONFIG FILE]: Not Found
 By default zellij looks for a file called [config.kdl] in the configuration directory
[CACHE DIR]: /home/hatch/.cache/zellij
[DATA DIR]: "/home/hatch/.local/share/zellij"
[PLUGIN DIR]: "/home/hatch/.local/share/zellij/plugins"
```

"Not Found" is the healthy answer on a
fresh machine: it means no config file
exists yet, so every setting is a default.
Zellij creates what it needs under those
directories as you use it; you do not have
to prepare any of them by hand.

While you are here, look at the size of
the program's surface — you will use a
small part of it daily, and the rest
exists for scripts and special cases:

```bash
zellij --help
```

The subcommands include `attach`,
`action`, `list-sessions`, `setup`, and
(in 0.45) `web` and `watch`. Each has its
own `--help`; `zellij action --help`
alone lists several dozen verbs, all of
which chapter 6 and the recipes put to
work.

## The check

You are installed when both of these say
so:

```text
$ zellij --version
zellij 0.45.1
$ zellij setup --check
[Version]: "0.45.1"
[CONFIG DIR]: Not Found
...
[CACHE DIR]: /home/you/.cache/zellij
```

(The paths carry your own home directory,
of course — the shape is what matters.)

Next chapter: start it.
