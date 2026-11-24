# shelly-stack

shelly-stack is Sean's fork of [pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT, by poteto / Lauren Tan) for Third Wave Discounts. It holds poteto's playbooks and principles, adapted to how we ship.

It helps an agent write less code of higher quality. It turns one coding agent into a small engineering team that reads first, verifies its work, and reviews before it ships.

This package runs on any model in any client that can read files and run a shell. That includes Claude, Codex, and Gemini through Antigravity, on their own or inside T3 Code or Orca. [`references/runtime.md`](./references/runtime.md) checks which app it runs in, then maps each action a skill names to that app's tools.

## Install

This one folder is a plugin for Claude Code, Codex, and Antigravity (Gemini). Set `SHELLY_ROOT` to this checkout.

```bash
SHELLY_ROOT=/absolute/path/to/shelly-stack
```

- Claude Code: `claude plugin marketplace add "$SHELLY_ROOT"`, then `claude plugin install shelly-stack@shelly-stack`. Or from GitHub: `/plugin install shelly-stack --marketplace thirdwavediscounts/shelly-stack`. The plugin also runs four hooks from `hooks/claude-hooks.json`: a destructive-SQL guard, its one-time approval, a status-line check, and a prompt list after compaction. It ships one helper agent, [`agents/shelly-agent.md`](./agents/shelly-agent.md). The lead picks its model and effort on each spawn.
- Codex: `codex plugin marketplace add "$SHELLY_ROOT"`, then `codex plugin add shelly-stack@shelly-stack`. Codex runs a copy in `~/.codex/plugins/cache`, so rerun `codex plugin add shelly-stack@shelly-stack` after every change. Each skill's `agents/openai.yaml` sets its Codex display name and whether Codex may start it on its own.
- Antigravity (Gemini): the repo root is an Antigravity plugin (`plugin.json`). Link it once into the plugins folder of each config root. Standalone Antigravity reads `$HOME/.gemini/config/`. T3 Code runs Antigravity with its own root, `$HOME/.t3/userdata/providers/antigravity/<id>/config/`.

```bash
for root in "$HOME/.gemini/config" "$HOME"/.t3/userdata/providers/antigravity/*/config; do
  mkdir -p "$root/plugins" && ln -sfn "$SHELLY_ROOT" "$root/plugins/shelly-stack"
done
```

- Orca: install the plugin for each agent you run in Orca (Claude Code, Codex, or Gemini), as above. Orca's own skills (`orca skills install`) let shelly-stack start Orca workers.
- Any other client: link each skill folder into its global skills folder.

```bash
SKILLS_DIR="$HOME/.agents/skills"
mkdir -p "$SKILLS_DIR"
for d in "$SHELLY_ROOT"/skills/*/; do ln -sfn "${d%/}" "$SKILLS_DIR/$(basename "$d")"; done
```

Use one install per client. A plugin and skill links together register the same skill names twice.

## Get started

1. Ask for the [`setup-shelly-stack`](./skills/setup-shelly-stack/SKILL.md) skill. It finds your models and writes `~/.config/shelly-stack/models-<app>.md` for the app you run it in (`claude`, `t3`, `orca`, `codex`, or `antigravity`), which picks a model and effort per role. Without it, every role runs on your current model.
2. Start any task that needs rigor with [`shelly-mode`](./skills/shelly-mode/SKILL.md). Say "use shelly-mode", then the goal and how you will know it is done.
3. Unsure which skill fits? Ask for [`shelly-help`](./skills/shelly-help/SKILL.md).

```
use shelly-mode. this pr has a subtle bug where the scroll drifts every 750ms even when idle.
repro first, then fix and verify.
```

shelly-mode matches the task to a playbook and posts its steps as a checklist. It runs the other skills (`how`, `why`, `architect`, `arena`, `shelly-swarm`, `interrogate`, `unslop`, `no-comments`, and the principles) as the steps need them. When you switch subjects, say "new task" so it matches a playbook again.

## Playbooks

| playbook | for |
|---|---|
| [investigation](./skills/shelly-mode/playbooks/investigation.md) | a read-only question. how does x work, why was y built this way, are we sure. |
| [bug fix](./skills/shelly-mode/playbooks/bug-fix.md) | reproduce a defect, root-cause it, and fix with runtime evidence. |
| [perf](./skills/shelly-mode/playbooks/perf-issue.md) | trace a measured slowness and improve it against a baseline. |
| [hillclimb](./skills/shelly-mode/playbooks/hillclimb.md) | sustained, scientific improvement of one metric against a target, looping hypotheses with before/after measurement and one commit per accepted win. |
| [runtime forensics](./skills/shelly-mode/playbooks/runtime-forensics.md) | diagnose a live symptom (leak, idle-cpu spin, glitch) from instrumentation. |
| [trace forensics](./skills/shelly-mode/playbooks/trace-forensics.md) | diagnose a captured profiling artifact (cpuprofile, trace, spindump, heap snapshot). |
| [feature](./skills/shelly-mode/playbooks/feature.md) | new or changed behavior, built from a named data shape. |
| [refactoring](./skills/shelly-mode/playbooks/refactoring.md) | a behavior-preserving change to structure or shape. |
| [prototype](./skills/shelly-mode/playbooks/prototype.md) | a throwaway sketch to make a design or behavioral decision cheaply, or to settle an empirical fork by observing it. |
| [visual parity](./skills/shelly-mode/playbooks/visual-parity.md) | pixel-exact ui equivalence between two implementations. |
| [authoring a skill](./skills/shelly-mode/playbooks/authoring-a-skill.md) | writing or editing a SKILL.md. |
| [eval](./skills/shelly-mode/playbooks/eval.md) | test how a skill or prompt change affects agent behavior, blinded. |
| [opening a pr](./skills/shelly-mode/playbooks/opening-a-pr.md) | turn finished work into a reviewable pr: small ordered commits, clean diff, open items folded in before merge. |
| [babysit](./skills/shelly-mode/playbooks/babysit.md) | drive a pr or a stack to merge-ready: conflicts, review threads, ci. |
| [shipping](./skills/shelly-mode/playbooks/shipping.md) | independently verify a green stack, then land the contiguous verified run one PR at a time with `gh pr merge --squash --auto`, or with Origin's merge-when-ready. |
| [autonomous run](./skills/shelly-mode/playbooks/autonomous-run.md) | drive a long task to completion without stopping. |
| [orchestrate](./skills/shelly-mode/playbooks/orchestrate.md) | a standing project handed to one coordinator chat: multi-day, many stacked prs, fleets of subagents. |
| [autopilot-full](./skills/shelly-mode/playbooks/autopilot-full.md) | run independent prs to merged with one owner per pr and root verification of each merge-ready head. |
| [autopilot-stack](./skills/shelly-mode/playbooks/autopilot-stack.md) | build and verify one linear base-branch stack for the operator to review and land. |
| [session pickup](./skills/shelly-mode/playbooks/session-pickup.md) | resume or take over a prior agent's in-flight work. |
| [pause safely](./skills/shelly-mode/playbooks/pause-safely.md) | suspend in-flight work cleanly so it can be resumed later. |
| [multi-phase plan](./skills/shelly-mode/playbooks/multi-phase-plan.md) | work that spans phases or stacked PRs. |
| [worktree cleanup](./skills/shelly-mode/playbooks/worktree-cleanup.md) | reclaim disk by pruning merged or abandoned worktrees and stale ios simulators, safety-gated. |

## Make it yours

- After a task that taught you something, ask for the [`reflect`](./skills/reflect/SKILL.md) skill. It proposes edits to the skills.
- When agents keep making the same mistake, ask for the [`correct`](./skills/correct/SKILL.md) skill. It fixes the repo so the mistake cannot come back.
- To change models or budget, run [`setup-shelly-stack`](./skills/setup-shelly-stack/SKILL.md) again.

## Claude Code cloud sessions

Cloud sessions do not carry over local `~/.claude`. The cloud environment's setup script clones this repo and runs `cloud/install.sh`. It installs the production Supabase guard, the stale-checkout warning, the tailnet join for `ssh twd`, the app env files from Infisical, and the Postgres tunnel over `ssh twd`.

## Checks

```bash
python3 tests/check_agnostic.py
python3 hooks/test_hooks.py
node --test cloud/prod-db-guard.test.mjs
```

The first fails when a skill or reference names one client's tools, agent types, models, or config paths.

## License

MIT, see [LICENSE](LICENSE).

- `thermo-nuclear-code-quality-review` is adapted from Third Wave Discounts' MIT-licensed Team Kit fork (see [LICENSE.team-kit](LICENSE.team-kit)).
- `untangle-codebase` is adapted from Caldo's MIT-licensed [skills](https://github.com/caldoai/skills) (see [LICENSE.caldo-skills](LICENSE.caldo-skills)).
- `grilling`, `wizard`, `pr`, the spec reviewer, and parts of the Bug fix playbook are adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (MIT, see [LICENSE.mattpocock-skills](LICENSE.mattpocock-skills)).
