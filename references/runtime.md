# Runtime contract

shelly-stack runs on any model in any client that can read files and run a shell. This file maps each thing a skill asks for to the tool that does it. Skills name the action ("load the `how` skill", "spawn a delegate on the `bug-fix` role"). This file says how. When a client offers a tool named here, use it. When it does not, use the fallback. When neither works, say which step could not run and why. Never pretend a step ran.

## Words used in every skill

- `<SHELLY_ROOT>` is the folder that holds `skills/`, `references/`, and `README.md` for this package. Find it from the path of any shelly-stack `SKILL.md` you loaded: it is two folders up. Put the absolute path in every brief you write. Never use `${CLAUDE_PLUGIN_ROOT}` or a guessed cache path.
- **Load a skill** means: call the client's skill tool with the skill's name when one exists and lists it. Otherwise read `<SHELLY_ROOT>/skills/<name>/SKILL.md` in full and follow it. Both count as loading it. Resolve the skill's own `references/` and `scripts/` paths from its folder.
- **Principles** (`principle-*`) are always read as files, never called as tools.
- **The task list** is the client's todo or plan tool. With none, post the steps as a `- [ ]` checklist in your reply and update it when a step's state changes.
- **Ask the user** means the client's question tool. With none, ask in your reply and end the turn.
- **A secret** comes from the client's secret request tool when one exists (T3 Code: `request_secret`). Otherwise follow the repository's instructions (for example `op run` or `op read`). Never ask for a secret in chat.

## Helpers (subagents)

A helper is another agent that gets only the brief you write. It does not see your conversation.

### Briefs

Every brief starts from one file under `<SHELLY_ROOT>/references/briefs/`, plus the task.

- `delegate.md`: a helper that writes code or runs a playbook step. It reads `skills/shelly-mode/SKILL.md` first.
- `reader.md`: a helper that answers one read-only question.
- `<SHELLY_ROOT>/references/maintainability-reviewer.md`, `spec-reviewer.md`, `ci-watcher.md`, and `briefs/comment-sicko.md`: reviewers.

Write the brief as: the absolute path of the brief file to read first, `<SHELLY_ROOT>`, the user's goal in one sentence, the task, file pointers (not pasted file bodies), what to return, and for any datastore the environment (staging or production) and a rule to print the target before the first write.

### Roles and models

Skills name a role, never a model. Roles: `feature, refactoring`, `bug-fix`, `perf-issue`, `hillclimb`, `judgment and prose`, `hardest tasks`, `how explorer`, `how explainer`, `why investigators`, `why synthesizer`, `reflect tooling`, `reflect judgment, divergent, synthesizer`, `arena runners`, `arena cross-judge pool`, `swarm workers`, `architect runners`, `interrogate reviewers`, `reader`.

1. Read `~/.config/shelly-stack/models.md`. Each line is `<role>: <value>`. A value is `inherit` (the parent's provider and model) or `<provider>/<model>` followed by optional `key=value` options, for example `claudeAgent/claude-opus-5-5 effort=high`. Panel roles hold a comma-separated list, and one helper runs per entry.
2. A role with no line, or no file, uses `inherit`.
3. Before the first cross-provider spawn in a thread, call `orchestrator_capabilities` once. A value whose provider or model is not in the catalog is unavailable. Say so and ask the user. Never switch provider or model on your own.
4. Before a fan-out, list each stage and its role value in your reply so the user can stop it before spend.
5. Effort: start from the role's value. Raise it one step for the hardest work, lower it for routine work. Pass it in the provider's option (the option id `orchestrator_capabilities` lists for that model, such as `effort`, `reasoningEffort`, or `thought_level`).

### Spawning

Pick the first path that fits:

1. **T3 Code `delegate_task`.** Use it for another provider's model, any option the parent does not have, a separate checkout (`isolation: "worktree"`), and every background helper. Pass `target: {providerInstanceId, model, options}` from the role value, `role` (`implementation`, `research`, `review`, `design`, `test`, `general`), `mode: "async"`, and a short `title`. Keep the returned `taskId`.
2. **The client's own subagent tool** (Claude Code `Agent`, Codex `spawn_agent`, Antigravity `invoke_subagent`). Use it when the helper runs on the parent's own provider and model with no extra options, and for read-only helpers when the client can enforce read-only (see below).
   - Claude Code without `delegate_task` (outside T3 Code): a `claudeAgent/<model>` value runs as `Agent` with `model` set to the model's short name (`opus`, `sonnet`, `haiku`, `fable`). Its effort options cannot be set there; the helper runs at the session's effort. A `codex/...` value runs as `Agent` with `subagent_type: "codex:codex-rescue"` when that plugin is installed, on the model set in `~/.codex/config.toml`. An `antigravity/...` value is unavailable there. Say so.
3. **No spawn tool.** Do the step yourself in sequence and say the step ran without an independent helper.

### Waiting

- Start helpers asynchronously, then continue other work. When none is left, end the turn. The helper's completion wakes you. Read the result then (`task_status` for `delegate_task`).
- Do not poll a running helper, sleep, loop in the shell, or schedule wakeups to wait for it.
- Cancel a helper you no longer need with `task_cancel` (or the client's equivalent). Start no replacement unless the work still needs one.
- A fan-out of N helpers is N async spawns in one turn. Cap N at the panel size or the skill's limit. The `Workflow` tool is used only when the user asked for a workflow.

### Read-only helpers and reviewers

- An enforced read-only helper is one the client sandboxes: Claude Code agents restricted to read tools, Antigravity `invoke_subagent` with `TypeName: "research"` or `define_subagent` with write tools off, a Codex read-only sandbox.
- `delegate_task` has no read-only mode. For a reviewer on another provider, spawn it with `isolation: "worktree"`. The worktree is a checkout of the T3 project the thread belongs to. For a repo outside that project, `delegate_task` cannot isolate the reviewer. Say so and ask the user.
- Before the spawn, record the real checkout's `git rev-parse HEAD`, `git branch --show-current`, and `git status --porcelain`. Tell the reviewer to work only in its own worktree and to leave untracked repro files there, never commits or edits to tracked files.
- When it returns, find its worktree with `t3_worktree_list` for the child's thread. Run `git -C <its worktree> status --porcelain --untracked-files=no` and `git -C <its worktree> log <base>..HEAD`. Both must be empty. Then rerun the three reads on the real checkout. They must match what you recorded. If anything differs, discard the review, report the breach, and restore or remove what it changed.
- `isolation: "worktree"` starts from the parent's last commit, so uncommitted edits are missing. Commit the work to a local branch first (a `sean/*` or scratch branch, not pushed), then spawn. Never create a helper's checkout by hand in the shell.
- Never call a writable helper read-only because its brief says so.

### Owning the result

You own every helper's work. Read its diff and write your own summary. A second opinion is the same brief on a different model. Agreement is a strong signal.

## PRs, CI, and history

- **PRs and CI.** Use the client's PR tools when they exist (T3 Code: `pull_request_read`, `pull_request_create`, `pull_request_update`, `pull_request_review`, `pull_request_respond`, `pull_request_merge`, `ci_logs`, `ci_rerun`, `watch_pull_request`). Otherwise use `gh` (`gh pr checks`, `gh run view --log-failed`). Resolve the PR head before and after you read checks. A stale result or an empty check set is not a pass.
- **Waiting on CI.** With `watch_pull_request`, watch and end the turn. Without it, check once per turn with bounded commands. A recurring check needs a scheduling tool (T3 Code: `schedule_task`) and either an explicit request or a playbook step that arms one for work the user handed off (autonomous run, multi-phase plan, babysit, a long bug hunt).
- **Earlier history.** Use the current conversation first. Then the client's thread tools (T3 Code: `t3_thread_search`, `t3_thread_read`, `t3_thread_list`). With none, use a transcript path the user gives. Never scan other projects' history.
- **Showing the user something mid-turn.** Use the client's send tool when one exists (T3 Code: `send_to_user`).

## Authorization

An explicit request to open or ship a PR includes focused commits, pushes, and opening or updating the PR. A review, test run, or local fix alone does not. CI repair may push when the request covers bringing the PR to green. Merge, deploy, send messages, or rewrite published history only when separately authorized. Never bypass required checks. Preserve unrelated changes and follow the repository's branch, commit, and PR rules.
