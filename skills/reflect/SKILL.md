---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

Invoke when the user says "reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, run `scripts/find-transcript.sh "$PWD" "<opening words of this conversation's first user prompt>"`. It derives the workspace's transcript directory (this workspace's own, never another project's, since those hold private chats) and prints the newest transcript whose first user message contains that prompt. It checks session transcripts before subagent transcripts. If it prints nothing, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One turn, three async helper spawns with the delegate brief. Reviewers use MCP tools to look up the tickets, chat threads, and observability traces the transcript references. The prompt forbids file writes. The parent applies edits.

Each reviewer and the synthesizer name a role line in `~/.config/shelly-stack/models.md`. Resolve it per `<SHELLY_ROOT>/references/runtime.md`. If a value is unavailable, say so and ask the user.

A configured role value is `inherit` or a provider and model with options, per `<SHELLY_ROOT>/references/runtime.md`.

| Lens | Role line | Prompt template |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the helper's result.

## 3. Synthesize

One helper with the delegate brief, on the `reflect judgment, divergent, synthesizer` role. It spot-verifies citations through MCP tools. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **encode-lessons-in-structure** principle (Read `../principle-encode-lessons-in-structure/SKILL.md`).

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File each Backlog item to your team's devex or backlog tracker without waiting. Only the Accepted list waits for approval.

Never edit a skill in the client's installed-skill cache. Before approval, show each edit's destination. A shelly-stack skill changes in a `sean/*` worktree of the plugin's source checkout. For any other plugin skill, the destination is the project or personal skills folder the client loads it from. After approval, copy the skill folder there and edit the copy. Never open a PR or push.

Follow each approved row's Routing exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): the parent does it directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the **create-skill** skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `create-skill` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `create-skill`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
