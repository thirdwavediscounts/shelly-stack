---
name: setup-shelly-stack
description: Configure which models shelly-stack uses per role and at what reasoning budget. Detects your available models and writes a user-level config file that overrides the skill defaults. Use for "set up shelly-stack", "configure shelly-stack models", "shelly-stack budget", or changing shelly-stack's model choices.
---

# Setup shelly-stack

Write the models file for the app you run in, `~/.config/shelly-stack/models-<app>.md`. Every shelly-stack skill reads it, then the shared `~/.config/shelly-stack/models.md`, to pick the model for each role. Run this skill once in each app whose models differ. `<SHELLY_ROOT>/references/runtime.md` (section "Roles and models") defines the format and how skills use it. Read that section first.

## Steps

### 1. Detect available models

Find your app and its file name in `<SHELLY_ROOT>/references/runtime.md` ("Find your app"). With no matching app, write the shared `models.md` in place of `models-<app>.md` everywhere below. Follow the **Models** line in its section to list the `<provider>/<model>` pairs it can run and each model's effort option and values. That list is the catalog. Use the option names and values it gives, never a guess.

If your app's section has no **Models** line, only `inherit` is available. If you cannot list the models, ask the user to paste the models and effort levels they have. Never write a value you have not confirmed. `inherit` is always valid.

### 2. Load current state

If `~/.config/shelly-stack/models-<app>.md` exists, read it. Otherwise read the shared `~/.config/shelly-stack/models.md` if it exists. The file you read is the current state. Its `# budget` line and role values are the current choices. Otherwise start from the defaults in step 5. Drop any line whose role is not in step 5, such as `how critics`. It is from a retired role.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Ask the user. Offer these four options with these exact labels. Name the current budget when the file records one. With no file, say that every role runs on the parent's model at the parent's effort.

- `unlimited, max reasoning`
- `large, xhigh reasoning`
- `medium, high reasoning`
- `small, medium reasoning`

**(b) Apply it.** Build the working table from the defaults. On a re-run, keep any role the user moved to another model, list, or `inherit`. The budget sets the effort option on every real value, panel entries included, to `max`, `xhigh`, `high`, or `medium`. The effort ladder is `max` > `xhigh` > `high` > `medium` > `low`. When a model's effort option has no value at the target, use the highest value it lists below the target. When a model has no effort option, leave the value bare. `inherit` does not change. For example, `large` on a model whose `thought_level` stops at `xhigh` writes `thought_level=xhigh`, and `unlimited` on the same model also writes `thought_level=xhigh`.

**(c) Show the roles and confirm.** Show every role with its value. Mark any real value not in the catalog as needing a choice. List each line step 2 dropped. Ask the user whether to accept as-is or change specific roles. Offer the catalog's models and `inherit` (the role runs on the parent's provider and model).

- Panel roles hold a comma-separated list, and one helper runs per entry, so the list length sets the count. They are `arena runners`, `arena cross-judge pool`, `architect runners`, and `interrogate reviewers`. Suggest one entry per available provider, because different models catch different things.
- `arena cross-judge pool` runs one judge. It tries entries whose model differs from the parent's, in list order, so order it by preference. An `inherit` entry never judges.
- `swarm workers` is the model for every `shelly-swarm` worker unless a race or comparison assigns another model per arm.

### 4. Validate

Check every real value against the catalog.

- `<providerInstanceId>/<model>` must be a pair from step 1.
- Each `key=value` option must be an option that model lists, with a value from its `values`.
- `inherit` always passes.

If a value fails, stop and ask the user again.

### 5. Write the file

Create `~/.config/shelly-stack/` if it is missing. Write `models-<app>.md` with the comment lines, a `# budget` line with the chosen label and its target effort, and one line per role. Overwrite the whole file so re-runs give the same result. Never put role lines in a repository's `AGENTS.md` or any other instructions file.

The shape below shows the defaults. Every role defaults to `inherit`. The second block shows real values after the user picks models with the `large` budget.

```
# shelly-stack model configuration. One line per role. Delete a line to fall back to inherit.
# Value: inherit, or <providerInstanceId>/<model> followed by key=value options. Panel roles take a comma-separated list, one helper per entry.
# budget: none
feature, refactoring: inherit
bug-fix: inherit
perf-issue: inherit
hillclimb: inherit
judgment and prose: inherit
hardest tasks: inherit
how explorer: inherit
how explainer: inherit
why investigators: inherit
why synthesizer: inherit
reflect tooling: inherit
reflect judgment, divergent, synthesizer: inherit
arena runners: inherit
arena cross-judge pool: inherit
swarm workers: inherit
architect runners: inherit
interrogate reviewers: inherit
reader: inherit
```

```
# budget: large (xhigh)
bug-fix: <providerA>/<model-1> effort=xhigh
swarm workers: <providerA>/<model-2> effort=xhigh
arena runners: <providerA>/<model-1> effort=xhigh, <providerB>/<model-3> reasoningEffort=xhigh, <providerC>/<model-4> thought_level=xhigh
```

### 6. Confirm

Tell the user which file was written and that it applies only in this app. Skills read it each time they spawn a helper, so it applies from the next spawn. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with the create-verification-skill skill." On yes, load the **create-verification-skill** skill. On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with the create-formal-verification-skill skill." On yes, load the **create-formal-verification-skill** skill. On no, move on without pushing.
