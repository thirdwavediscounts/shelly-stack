# Runtime contract

shelly-stack runs on any model in any client that can read files and run a shell. This file maps each thing a skill asks for to the tool that does it. Skills name the action ("load the `how` skill", "spawn a delegate on the `bug-fix` role"). This file says how. When a client offers a tool named here, use it. When it does not, use the fallback. When neither works, say which step could not run and why. Never pretend a step ran.

## Words used in every skill

- `<SHELLY_ROOT>` is the folder that holds `skills/`, `references/`, and `README.md` for this package. Find it from the path of any shelly-stack `SKILL.md` you loaded: it is two folders up. Put the absolute path in every brief you write. Never use `${CLAUDE_PLUGIN_ROOT}` or a guessed cache path.
- **Load a skill** means: call the client's skill tool with the skill's name when one exists and lists it. Otherwise read `<SHELLY_ROOT>/skills/<name>/SKILL.md` in full and follow it. Both count as loading it. Resolve the skill's own `references/` and `scripts/` paths from its folder.
- **Principles** (`principle-*`) are always read as files, never called as tools.
- **The task list** is the client's todo or plan tool. With none, post the steps as a `- [ ]` checklist in your reply and update it when a step's state changes.
- **Ask the user** means the client's question tool. With none, ask in your reply and end the turn.
- **A secret** comes from the client's secret request tool when one exists. Otherwise follow the repository's instructions (for example `op run` or `op read`). Never ask for a secret in chat.

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

1. Read the role's line from your app's models file, `~/.config/shelly-stack/models-<app>.md`. `<app>` is the file name "Find your app" gives your app. If that file has no line for the role, read the shared `~/.config/shelly-stack/models.md`. These two files are "your models file" in every skill. Each line is `<role>: <value>`. A value is `inherit` (the parent's provider and model) or `<provider>/<model>` followed by optional `key=value` options, for example `claudeAgent/claude-opus-5-5 effort=high` or `codex/gpt-6.2-sol reasoningEffort=xhigh`. Panel roles hold a comma-separated list, and one helper runs per entry.
2. A role with no line in either file uses `inherit`.
3. A value your app cannot run is unavailable. Say so and ask the user. Never switch provider or model on your own.
4. Before a fan-out, list each stage and its role value in your reply so the user can stop it before spend.
5. Effort: start from the role's value. Raise it one step for the hardest work, lower it for routine work. Pass it the way your app's section below says.

## Find your app

Check in this order. Use the first that matches, and only its section.

1. **T3 Code** (file name `t3`): you have a `delegate_task` tool.
2. **Orca** (file name `orca`): your shell has `ORCA_TERMINAL_HANDLE` set (`printenv ORCA_TERMINAL_HANDLE`). Orca sets it in every terminal it runs, and its worker commands need it.
3. **Claude Code**, CLI or desktop (file name `claude`): you have an `Agent` tool.
4. **Codex** (file name `codex`): you have a `spawn_agent` tool.
5. **Antigravity**, Gemini (file name `antigravity`): you have an `invoke_subagent` tool.
6. **None of these:** do each helper step yourself, in order, and say it ran without an independent helper. Read only the shared models file.

Every app follows the shared rules after these sections.

### T3 Code

- **Models.** Before the first `delegate_task` in a thread, call `orchestrator_capabilities` once. Keep providers whose `canRunChildTask` is true and that list no constraint such as "disabled". Each pair is `<providerInstanceId>/<model id>`, with the model's options and allowed `values`. The effort option is named per model (`effort`, `reasoningEffort`, or `thought_level`). If a model the user names is missing (`omittedModels`), call it again with `search` set to that name. A value not in the catalog is unavailable.
- **Start a helper.** `delegate_task` with `target: {providerInstanceId, model, options}` from the role value, `role` (`implementation`, `research`, `review`, `design`, `test`, or `general`), `mode: "async"`, and a short `title`. Add `isolation: "worktree"` for a helper that writes or reviews. Keep the returned `taskId`.
- **Wait and stop.** Read the result with `task_status` when the helper wakes you. Stop one with `task_cancel`.
- **Read-only.** `delegate_task` has no read-only mode. Spawn reviewers with `isolation: "worktree"` and check them per the shared rules. Find the reviewer's worktree with `t3_worktree_list`. For a repo outside the thread's T3 project it cannot isolate a reviewer. Say so and ask the user.
- **Other tools.** Secrets: `request_secret`. PRs and CI: `pull_request_read`, `pull_request_create`, `pull_request_update`, `pull_request_review`, `pull_request_respond`, `pull_request_merge`, `ci_logs`, `ci_rerun`, `watch_pull_request`. Recurring checks: `schedule_task`. History: `t3_thread_search`, `t3_thread_read`, `t3_thread_list`. Showing the user something mid-turn: `send_to_user`.

### Orca

- **Models.** Orca starts the `claude`, `codex`, and `gemini` agents. Use `claudeAgent/<claude model id>` with `effort` (`low`, `medium`, `high`, `xhigh`, `max`), `codex/<slug>` from `.models[].slug` in `~/.codex/models_cache.json` with `reasoningEffort`, and `antigravity/<model>` for Gemini. Leave out an agent whose CLI is not installed (`command -v claude codex gemini`).
- **Load Orca's guide once.** Run `orca skills get orchestration` and follow it for every command below. Use `$ORCA_CLI_COMMAND` in place of `orca` when it is set.
- **Start a helper.** Write the brief to a file. Run `orca orchestration worker-start --environment local --spec-file <brief file> --agent <agent> --model <model> --effort <effort> --worktree <where> --task-title "<title>"`. The agent comes from the role value's provider: `claudeAgent` is `claude`, `codex` is `codex`, `antigravity` is `gemini`. `inherit` is the agent you run as, with no `--model`. Use `--worktree new-child --name <short-name>` for a helper that writes or reviews, and `--worktree current` for a reader. Start up to four at once, then end your turn.
- **Wait and stop.** Orca wakes you with each worker's report. Read recent output with `orca orchestration worker-read --dispatch <id>`. Steer with `orca orchestration send --to dispatch:<id>`. Never poll or read a worker's terminal.
- **Read-only.** Orca has no read-only mode. Spawn reviewers in a `new-child` worktree and check them per the shared rules.
- **Other tools.** PRs and CI: `gh`. History: `orca search`. Linear: the `orca-linear` skill.

### Claude Code

- **Models.** The catalog is `claudeAgent/<model id>` for the Claude models (`claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, `claude-fable-5-2`) with `effort` (`low`, `medium`, `high`, `xhigh`, `max`), plus `codex/<slug>` from `.models[].slug` in `~/.codex/models_cache.json` with `reasoningEffort` when the Codex companion below exists. A `claudeAgent/<model>` value runs on the `Agent` tool with `model` set to the short name in the model id (`opus`, `sonnet`, `haiku`, `fable`). Pass the value's effort option as the `Agent` tool's `effort`. `inherit` omits both.
- **Start a helper.** A delegate is `Agent` with `subagent_type: "shelly-stack:shelly-agent"`, `run_in_background: true`, and the brief as `prompt`. A reader is `Agent` with `subagent_type: "Explore"`. Add `isolation: "worktree"` for a helper that writes in parallel with others or reviews.
- **Codex seats.** A `codex/<model>` value runs through the Codex plugin's companion script, not the `Agent` tool:
  1. Find it: `ls ~/.claude/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs | sort -V | tail -1`. If none exists, the value is unavailable.
  2. Write the full brief to a file.
  3. Run `node <script> task --fresh --model <model> --effort <effort> --cwd <seat folder> --prompt-file <brief file>` with the Bash tool's `run_in_background: true`. Effort is one of `none`, `minimal`, `low`, `medium`, `high`, `xhigh`. Add `--write` for a seat that edits files in its own worktree. Leave it out for a reviewer or judge, which then runs in Codex's read-only sandbox.
  4. When it ends, its stdout is the reply. A nonzero exit or empty reply drops the seat. Name the reason from the first line of output and go on with the other seats.
- **Other providers.** An `antigravity/...` value is unavailable. Say so.
- **Wait and stop.** Background helpers wake you when done. Stop one with `TaskStop`. The `Workflow` tool runs only when the user asked for a workflow.
- **Read-only.** No Claude helper is read-only: `Explore` and `Plan` lack edit tools but keep the shell. Spawn reviewers with `isolation: "worktree"` and check them per the shared rules. Codex seats without `--write` are read-only.
- **Other tools.** Ask the user: `AskUserQuestion`. Task list: the todo tool. PRs and CI: `gh`. History: read only this workspace's `~/.claude/projects/<slug>/` folder, where every character of the absolute workspace path that is not a letter, digit, or `-` becomes `-`.

### Codex

- **Start a helper.** `spawn_agent` with the brief. It runs on your own model. Another provider's value is unavailable. Say so.
- **Read-only.** Spawn reviewers in Codex's read-only sandbox.
- **Other tools.** PRs and CI: `gh`.

### Antigravity (Gemini)

- **Start a helper.** `invoke_subagent` with the brief. It runs on your own model. Another provider's value is unavailable. Say so.
- **Read-only.** `invoke_subagent` with `TypeName: "research"`, or `define_subagent` with write tools off.
- **Other tools.** PRs and CI: `gh`.

## Shared rules for helpers

### Waiting

- Start helpers asynchronously, then continue other work. When none is left, end the turn. The helper's completion wakes you.
- Do not poll a running helper, sleep, loop in the shell, or schedule wakeups to wait for it.
- Stop a helper you no longer need. Start no replacement unless the work still needs one.
- A fan-out of N helpers is N async spawns in one turn. Cap N at the panel size or the skill's limit.

### Reviewers in a worktree

- `isolation: "worktree"` and Orca's `new-child` start from the last commit, so uncommitted edits are missing. Commit the work to a local branch first (a `sean/*` or scratch branch, not pushed), then spawn. Never make a helper's checkout by hand.
- Before the spawn, record the real checkout's `git rev-parse HEAD`, `git branch --show-current`, and `git status --porcelain`. Tell the reviewer to work only in its own worktree and to leave untracked repro files there, never commits or edits to tracked files.
- When it returns, run `git -C <its worktree> status --porcelain --untracked-files=no` and `git -C <its worktree> log <base>..HEAD`. Both must be empty. Then rerun the three reads on the real checkout. They must match. If anything differs, discard the review, report the breach, and restore or remove what it changed.
- Never call a writable helper read-only because its brief says so.

### Owning the result

You own every helper's work. Read its diff and write your own summary. A second opinion is the same brief on a different model. Agreement is a strong signal.

## PRs, CI, and history

- **PRs and CI.** Use your app's PR tools when its section names them. Otherwise use `gh` (`gh pr checks`, `gh run view --log-failed`). Resolve the PR head before and after you read checks. A stale result or an empty check set is not a pass.
- **Waiting on CI.** With a PR watch tool, watch and end the turn. Without one, check once per turn with bounded commands. A recurring check needs a scheduling tool and either an explicit request or a playbook step that arms one for work the user handed off (autonomous run, multi-phase plan, babysit, a long bug hunt).
- **Earlier history.** Use the current conversation first. Then your app's history tool or folder. With none, use a transcript path the user gives. Never scan other projects' history.

## Authorization

An explicit request to open or ship a PR includes focused commits, pushes, and opening or updating the PR. A review, test run, or local fix alone does not. CI repair may push when the request covers bringing the PR to green. Merge, deploy, send messages, or rewrite published history only when separately authorized. Never bypass required checks. Preserve unrelated changes and follow the repository's branch, commit, and PR rules.
