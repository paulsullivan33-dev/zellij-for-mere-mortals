# Plugins and the Web Server

**Outcome: you know which parts of the
screen are plugins, can open the plugin
managers, can write the built-in plugins
out to disk to see what they are — and
can serve a session to a web browser,
with a login token, and shut it down
again.**

## Plugins are panes

Chapter 2 made the claim; here is the
proof by inventory. Ask for the built-in
plugins as files:

```bash
zellij setup --dump-plugins ./plugins-out
```

The lab's directory filled with a
`plugins/` folder of WebAssembly
modules, each roughly one to two
megabytes:

```text
about.wasm           layout-manager.wasm
compact-bar.wasm     link.wasm
configuration.wasm   multiple-select.wasm
plugin-manager.wasm  session-manager.wasm
share.wasm           status-bar.wasm
strider.wasm         tab-bar.wasm
```

These run in panes, sandboxed, and the
ones you already know are in the list:
`tab-bar`, `status-bar`, `about`. The
short names layouts use are aliases:

```bash
zellij list-aliases
```

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

## The managers

Three plugins run the place, all in
**Session mode** (Ctrl o):

| Key | Plugin | What it does |
|-----|--------|--------------|
| `w` | session-manager | list sessions; attach, kill, save |
| `p` | plugin-manager | see loaded plugins, load new ones |
| `c` | configuration | edit configuration in place |
| `l` | layout-manager | browse and apply layouts |
| `a` | about | the About pane |
| `s` | share | session sharing (below) |

The session manager opens as a floating
pane listing the *other* sessions too.
The lab, attached to one session with a
second one running, read its screen from
outside:

```text
Session: _

lab-other 1t, 2p, 0c [ATTACH] <TAB> Complete

<Ctrl r>/<Ctrl x>/<Del>
<Ctrl a> - Save session (not saved)
```

That last line is chapter 9's force-save,
wearing a key: Ctrl a in the manager
saves the session it points at.

Third-party plugins load from a file or a
URL with the pipe of chapter 6's world —
`zellij plugin -- file:/path/to.wasm` —
and writing your own is a Rust (or other
wasm-targeting language) project, out of
this guide's scope as the README said.
Downloaded plugins live under the data
directory, `~/.local/share/zellij/plugins`.

## Sharing, properly

Session mode's `s` (the `share` plugin)
and the `watch` command of chapter 9 are
two strengths of the same thing: watch is
a terminal-only, read-only guest;
sharing a session through the web server
(below) extends the reach to a browser.
Both inherit chapter 1's rule — a guest
who can type is a guest who can run
commands.

## The web server

New in 0.45, Zellij can serve sessions
over HTTP, so a browser becomes a client:

```bash
zellij web --daemonize
```

```text
Web Server started on 127.0.0.1 port 8082
```

```bash
zellij web --status
```

```text
Web server online with version: 0.45.1. Checked: http://127.0.0.1:8082
```

The address is localhost by default, and
that default is the safe one: the server
is for *your* browser on *your* machine
(or tunnelled to you — an SSH tunnel is
the SSH guide's business). Binding beyond
localhost requires TLS certificate
arguments, by design.

Access is by login token. A token is
shown **once**, at creation:

```bash
zellij web --create-token
```

```text
Created token successfully

token_1: ***
```

(the lab redacted its token in the
transcript and revoked it immediately
after; do the same discipline with yours:
`zellij web --list-tokens` shows names
and dates, never values;
`--revoke-token` and `--revoke-all-tokens`
take them back.)

What the lab could verify headlessly, it
did: the server starts and reports
online; the root page answers HTTP 200,
and its title is `Zellij Web Client`.
What it could not do without a browser —
log in with the token, attach from the
page, type into a pane — is documented
only, and criteria.md files it there.
Sessions opt in to web access rather
than being exposed by default — the
`web_server` option's help puts it as
"attaching to existing ones that have
opted in", a `web_sharing` option
exists in the config, and the saved
session metadata of chapter 9 records
`web_clients_allowed false` for a
session that never opted in. Shut down
is one word:

```bash
zellij web --stop
```

```text
Stopped web server.
```

## The check

Dump the plugins and count them (twelve
files), open the session manager with
Ctrl o, `w` and close it with Esc, then
start the web server, confirm
`zellij web --status` says online and
`curl -s -o /dev/null -w '%{http_code}'
http://127.0.0.1:8082/` prints `200`,
and stop the server again. Everything in
this chapter except typing into the
browser page itself is now something you
have seen work.
