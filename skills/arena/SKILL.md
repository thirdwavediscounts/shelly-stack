---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for 'arena this', 'throw it in the arena', or when the architect skill or a shelly-mode playbook calls for a bakeoff."
---

# Arena

Open the task list (per `<SHELLY_ROOT>/references/runtime.md`) with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Use the `arena runners` line in your models file (per `<SHELLY_ROOT>/references/runtime.md`). If neither file has that line, run three runners on `inherit`. An `inherit` entry means the parent's provider and model. If an entry is unavailable per `<SHELLY_ROOT>/references/runtime.md`, say so and ask the user. If unavailable entries leave fewer than two runners, ask the user before continuing. Spawn more runners when the arena covers multiple design directions. Use the same role value N times when the work is generation-bound rather than judgment-sensitive. Spawn each runner as a helper with the delegate brief, per `<SHELLY_ROOT>/references/runtime.md`.
4. Give each candidate its own output location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle (Read `../principle-separate-before-serializing-shared-state/SKILL.md`).

## Phase B: Fan out

Spawn all N subagents in one message, each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one entry from the `arena cross-judge pool` line in your models file (per `<SHELLY_ROOT>/references/runtime.md`). If neither file has that line, use the other runners' entries. The judge is never the parent's model. An `inherit` entry is the parent model, so it never judges. Try the other entries in pool order. If an entry is unavailable per `<SHELLY_ROOT>/references/runtime.md`, move to the next one. If none runs, skip the judge, pick the base alone in Phase D, and say so. Spawn one judge as a read-only helper per `<SHELLY_ROOT>/references/runtime.md`. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't spawn it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle (Read `../principle-redesign-from-first-principles/SKILL.md`), so the result stays coherent under one mental model. Don't paste mechanically.

A graft that only adds a guard, check, or edge-case branch must name the real event it stops under the system's actual schedule and data. Reject it otherwise. Grafting adds by default, so every added guard must earn its place with a named event.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle (Read `../principle-prove-it-works/SKILL.md`). If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
