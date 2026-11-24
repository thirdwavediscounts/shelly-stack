---
name: create-skill
description: Author or edit a SKILL.md. Use for "create a skill", "write a skill for X", "turn this into a skill", or when another shelly-stack skill (reflect, the authoring-a-skill playbook) says to use create-skill. Covers frontmatter, placement, triggering, and the writing rules agents actually follow.
---

# Create skill

shelly-stack bundles this skill because most clients have no built-in. It sets the file shape; the **unslop** and **technical-writing** skills set the prose.

## Placement

- Project skill: `.agents/skills/<name>/SKILL.md`. Committed, shared with the team. Codex and Antigravity read that folder. A client that reads only its own folder (such as `.claude/skills/`) gets a link to it.
- Personal skill: the client's personal skills folder, in a `<name>/SKILL.md` folder. Just you, every project.
- Plugin skill: `<plugin>/skills/<name>/SKILL.md`. Ships with the plugin.

`<name>` is kebab-case and is the skill's name. Supporting files sit beside `SKILL.md` in `references/`, `scripts/`, or `playbooks/` and are referenced by relative path. A skill that needs an absolute path to its own files uses `<SHELLY_ROOT>/skills/<name>/...`. Supporting files use paths relative to the skill folder.

## Frontmatter

```yaml
---
name: <kebab-case, matches the directory>
description: <one YAML scalar; when to use it, in the user's words, trigger phrases included>
user-invocable: false            # every principle-* skill, and only those; hides it from the / menu
disable-model-invocation: true   # the same skills; keeps it off the model's skill list
argument-hint: "<what to pass after /name>"   # optional; shown in autocomplete
allowed-tools: Read, Grep, Glob  # optional; pre-approves these tools for the invoking turn, it restricts nothing
disallowed-tools: <tool name>  # optional; removes tools while the skill is active
---
```

Rules:

- `description` is the only text Claude sees before deciding to load the skill. Put the triggers there ("Use for X, Y, or when the user says Z"), not a summary of the body. Quote it or use `description: >-` when punctuation or wrapping needs it. The skill listing truncates `description` plus `when_to_use` at 1,536 characters, so put the key use case first.
- Set `user-invocable: false` and `disable-model-invocation: true` on every `principle-*` skill and on no other skill. `skills/shelly-mode/scripts/check_routing.py` fails CI otherwise. Antigravity reads only the second, and its skill list has a size budget that the principles would fill. Every other skill stays runnable by both the user and the agent. To keep a heavy skill from firing on casual turns, narrow its description to explicit requests and the skills that call it.
- The client ignores a key it does not recognize without an error, so a misspelled key is a silent no-op. Other documented keys (`when_to_use`, `arguments`, `model`, `effort`, `context: fork` with `agent`, `hooks`, `paths`) are for special cases; the full table is in the client's skill docs.
- `$ARGUMENTS` in the body is replaced with whatever the user typed after `/name`.

## Body

Write for an agent that will follow it under load, per the **technical-writing** skill:

- Lead with what the skill does and when. One paragraph.
- Use a numbered list where order matters or only one sequence is safe (destructive commands, auth, deploys), each step ending in a checkable state. For judgment work, state the outcome, the constraints, and how to verify. Name the action (spawn a helper, ask the user, run a command) and the model role when a step delegates.
- Reference sibling files by relative path. Reference other skills by bold name ("the **how** skill") so the reader knows to load them, and never paste their contents. A `principle-*` skill sets `user-invocable: false` and `disable-model-invocation: true`, so the client does not list it and its skill tool refuses it. Name it by the relative path to its `SKILL.md` and say to read it, as in "Read `../principle-prove-it-works/SKILL.md`".
- Say what the reply must contain. A skill that ends without an output contract produces a different reply every run.
- Cut anything the agent already knows. A skill is not a manual.

Every line goes through the **unslop** skill. No long dashes, no colon-as-connector, no "let's", no hedging.

## Check it

1. `/<name>` loads it and the first paragraph tells you what happens next.
2. The description alone, read cold, says when to use it and when not to.
3. A second agent given only the skill produces the same shape of output you did.

Reply: the path written, the trigger phrases in the description, and anything the skill assumes the project provides (a verify skill, an MCP, a script).
