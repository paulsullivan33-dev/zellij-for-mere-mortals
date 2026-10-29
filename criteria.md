# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's fixtures are a generic three-tab "workbench"
   layout and stock shell commands.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: resurrection restores the arrangement, not a
   program's state; quitting and killing are final; a misspelt
   config option fails silently; unknown layout names dump
   nothing, successfully; deletion messages can mislead;
   sharing is all-or-nothing per client; and the web client
   is young.
8. **The ethics rule is in the text, early.** Zellij raises a
   sharing question most tools in this series do not: anyone
   who can attach to a session sees everything in it,
   including passwords typed into panes. Chapter 1 and the
   README draw that line plainly — attach rights are shell
   rights — and the sessions and web chapters repeat it where
   the reader acts on it, before any procedure depends on it.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other work while the lab ran (shared-machine timing
shows up in the transcripts as occasional retries, which the
scenarios keep visible rather than smoothing over). Zellij
**0.45.1** was run from the official release archive
`zellij-x86_64-unknown-linux-musl.tar.gz`: the extracted
binary's SHA-256 matched the project's published checksum file
before anything else ran. The binary itself is not in this
repository; the lab's driver, scenario scripts, fixture files
and transcripts are, under `zellij-lab/`. Interactive sessions
were driven through a real pseudo-terminal by the lab's Python
driver (`zellij-lab/drive.py`), so every key sequence in the
chapters was sent to a live client, and every claim about the
session's shape was read back through the server's own action
commands rather than inferred from the screen.

Run for real, with transcripts as evidence:

- Version and the full `--help` surface — top level, `setup`,
  `options`, and the complete `action` verb list (t00, t01,
  t03).
- `setup --check` on a machine with no config (directories
  "Not Found", the healthy fresh state) and on configured
  ones; the full default config from `setup --dump-config`,
  which is also the source of every default keybinding the
  chapters tabulate (t01, t02, t07).
- The default and compact layouts dumped, and the classic and
  strider layouts; `dump-layout` of an unknown name printing
  nothing with exit 0 (t03, t09).
- A first session: the About/Release Notes pane opening
  focused, Esc dismissing it, a command running, and Ctrl q
  ending the session outright (t04).
- Panes and tabs at the keyboard: Ctrl p splits, per-pane
  `dump-screen` proving which pane held what, a second tab,
  a CLI rename read back by `query-tab-names`, and a full
  `dump-layout` of the result (t05).
- Layout files: a three-tab KDL layout (one pane running a
  command) starting a session; the same layout bare vs with a
  `default_tab_template`, compared through `dump-layout`;
  `--layout` adding a tab to a running session; a session
  dumped to a file and a fresh session started from the dump,
  tabs reproduced; a layout loaded by name from
  `~/.config/zellij/layouts/`; a broken layout producing the
  line-precise parse diagnostic and no session (t06).
- The config file: a working config (`theme`, `pane_frames
  false`, the two `show_` switches off, one added keybinding)
  reported "Well defined." by `setup --check`, applied in a
  live session — the welcome pane absent, and the config's
  own Alt w binding closing the pane Alt n opened; an
  unknown option silently ignored with the same "Well
  defined."; a syntax-error config failing loudly in both
  `--check` and session start (t07).
- The session lifecycle: background creation, attach, detach
  (work and screen intact on re-attach), rename from outside,
  kill (final — nothing listed, nothing resurrectable),
  delete refused on a running session and forced with
  `--force`; and the crash test — a session's server process
  killed with SIGKILL, the session listing as EXITED, and
  attach resurrecting the tab (by its renamed name) and both
  panes, with fresh shells. The saved state's files
  (`session-layout.kdl`, `session-metadata.kdl`) were listed
  and read (t08).
- Modes: Scroll mode paging back through 60 numbered lines to
  the top; Locked mode passing Ctrl p, `r` through to the
  shell as literal input (the prompt showed `^Pr`), a command
  running while locked, and the same two keys splitting the
  pane at once after unlocking (t11).
- Plugins: `list-aliases`; `setup --dump-plugins` writing the
  twelve built-in .wasm modules (1.2–1.8 MB each); the
  session manager opened with Ctrl o, `w` and its screen read
  from outside, showing the second session and its
  save-session key (t10).
- Actions from inside a session: `zellij action new-pane --
  <command>` typed at a pane's own prompt opened a pane
  running the command, verified from outside (t13).
- The web server: started daemonised, `web --status` online,
  a login token created (value redacted in the transcript and
  revoked immediately), the root page answering HTTP 200 with
  the title "Zellij Web Client", all tokens revoked, server
  stopped, status offline (t10).
- Watching: a read-only client (`zellij watch`) attached to a
  shared session; its typed command never reached the pane,
  while the normal client's did (t12).

Documented only — described from the project's documentation
and help output, not run, and the text does not claim
otherwise:

- Using the web client in a browser: logging in with a token,
  attaching from the page, typing into a pane. The server,
  tokens and page response above are verified; the browser
  session itself is not.
- Sessions opted into web sharing beyond the defaults (the
  `web_server` / `web_sharing` options) and TLS for
  non-localhost binds: named from help and config text; the
  lab bound localhost only, as the chapter teaches.
- Writing or loading third-party plugins, including plugin
  permissions and the plugin pipe; only the built-in plugins
  were exercised.
- Themes and pane-frame appearance: the lab set
  `theme "nord"` and `pane_frames false` and the config was
  provably read (the welcome pane vanished and the config's
  own keybinding worked), but a headless lab cannot see
  colours or borders, so how either looks is not graded here.
- The neighbours of chapter 12 (tmux, GNU Screen, terminal
  emulator tabs): characterised, not run or benchmarked,
  exactly as that chapter says.
- Install routes other than the official binary (package
  managers, Homebrew, cargo) and Zellij under WSL.
- Mouse interaction (dragging borders, click-to-focus,
  select-to-copy): the terminal driver is keystroke-based,
  so the mouse defaults are stated from the documentation.
- `serialize_pane_viewport` and other resurrection-adjacent
  options read from the default config but not toggled.

Fixtures are this guide's own and deliberately generic: a
three-tab "workbench" layout (an idle pane, a pair, a worker
running a print-and-sleep stand-in), a deliberately broken
copy of it, one invented config option (`banana_mode`), and
numbered lines from `seq`. No names, organisations, real
networks or real work appear anywhere in the lab.
