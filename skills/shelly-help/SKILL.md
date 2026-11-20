---
name: shelly-help
description: "Help for using shelly-stack (formerly shelly-guide): setup, shelly-mode, and picking the skill, playbook, or principle for a task or stage (understand, design, build, clean, verify, ship, overnight), with a copyable prompt for the actual task. Use for \"shelly-help\", \"shelly-guide\", \"how do I use shelly-stack\", \"which skill should I use\", \"what do I run now\", \"guide me through this with shelly-stack\", or a run that went wrong."
argument-hint: "[your question, what you're trying to do, or a stage name]"
---

# shelly-stack help

Answer the user's question about shelly-stack, hand them a prompt they can send, and link the file the answer came from. For a help question, don't start the work. The user asked how, and a shelly-stack run spends real tokens, so offer the prompt and let them say yes.

A message that asks for work, such as "use shelly-stack to fix this bug", is not a help question. Load the **shelly-mode** skill and do the task, or spawn a helper with the delegate brief (`<SHELLY_ROOT>/references/briefs/delegate.md`) as `<SHELLY_ROOT>/references/runtime.md` describes.

This file maps questions to the skills and playbooks that hold the answers. Those files own the details. Read the file you route to before you quote it, and trust it when it disagrees with this map. Skills live at `<SHELLY_ROOT>/skills/<name>/SKILL.md`. Playbooks live at `<SHELLY_ROOT>/skills/shelly-mode/playbooks/`. Link the local file by its absolute path.

## 1. Find out what they need

Read the user's arguments and the conversation. A named situation, such as "which skill reviews a PR?", goes straight to its section. A named stage goes to that stage in section 4. If the need is still unclear, ask the user one question with these options, then answer only the one they pick:

- Get set up
- Start a task with shelly-mode
- Pick a skill for the stage I'm at
- Fix a run that went wrong
- Make shelly-stack my own

For a stage question, ask for the task in their own words if they haven't given one. The prompt you hand back must be about their code, not a placeholder.

Check the state that changes the answer, and mention it only when it does:

- No `~/.config/shelly-stack/models.md` means the `setup-shelly-stack` skill hasn't run for this user, so every role runs on the parent's model.
- No `verify-*` skill or other app harness in the project means agents have no scripted way to drive the app. Mention the `create-verification-skill` skill when the question is about proving a change works.
- No formal verification skill in the project means no property is checked past what tests reach. Mention the `create-formal-verification-skill` skill when the question is about a race, an invariant, or another case tests rarely hit. When one exists and the code it covers changed after the commit it records as last in sync, mention the `maintain-formal-verification-skill` skill if the question touches that code.

When the models file is missing and it matters (the user is new, the question is about setup or cost, or the answer depends on which models run), ask once per chat whether they want to pick models now. Now: point them to the `setup-shelly-stack` skill and answer the question too. Later: answer, and add one line saying every role runs on the parent's model until they run it.

## 2. Get set up

Source: `<SHELLY_ROOT>/README.md` and `<SHELLY_ROOT>/skills/setup-shelly-stack/SKILL.md`.

1. Install by linking each skill folder into the client's skills folder. The README lists the folder for each client.
2. Ask for the `setup-shelly-stack` skill. It maps a model to each role and writes `~/.config/shelly-stack/models.md`. `inherit` means the role runs on the parent's provider and model. It is not a model name. A value can also set an option, such as the effort level.
3. Ask for the `create-verification-skill` skill when the project has no scripted way to drive the real app.
4. Start a real task with shelly-mode, a goal, and a check that can pass or fail.

If cost is the worry, say where the tokens go. shelly-stack spends extra tokens on helpers and review panels. Rerun `setup-shelly-stack` and pick cheaper models, a lower budget, or `inherit`. A shorter panel list runs fewer helpers, one per entry. Save shelly-mode for work that needs rigor.

## 3. Start a task with shelly-mode

Source: `<SHELLY_ROOT>/skills/shelly-mode/SKILL.md`. "Use shelly-mode to <goal + how you'll know it's done>" matches the task to a playbook, copies its steps into the task list, and runs the other skills as the steps need them. A skipped step stays in the list as `skip: <reason>`. A good prompt states the goal and the done check. It doesn't list skills, because a hand-written order drops or reorders steps the playbook keeps. Read [`references/prompting.md`](references/prompting.md) before you help word one.

- shelly-mode attaches to one message and fades as the chat moves on. Start each new task with it, or say "new task" to re-match a playbook.
- "don't change any code yet" pins Investigation.
- Ask for "a fresh worktree off <base>" when agents run in parallel.
- To get the same style from a helper of your own, give it the delegate brief at `<SHELLY_ROOT>/references/briefs/delegate.md`.

## 4. Pick a skill by stage

The default answer is shelly-mode, which runs most of the others when its steps need them. Name a skill directly when the user wants more or less of something than the playbook gives. Each stage gives the skills and the one pitfall.

**Understand.** `in-your-own-words` to check the agent understood the goal and problem before it starts. `sharpen` to rewrite a prompt deeper, not bigger. It returns the prompt and doesn't do the task. `how` for what the code does now. `why` for how it got this shape. `teach` when a summary isn't enough ("convince me it fixes the cause"). `recall` to rebuild your own recent context on a topic. `ketchup` to catch up on this chat since your last message, with every call waiting on you. `ketchup-video` gives the same as a short subtitled video. The Session pickup playbook ("use shelly-mode to take over this branch") is for an in-flight branch. Pitfall: skipping this because "the agent reads the code anyway".

**Design.** `grilling` first when the open questions are product decisions only you can make. A small finished change you're unsure about gets `interrogate` alone. A change to a type, an exported signature, or a module boundary gets `architect`, which brings `arena`. A standalone decision (naming, format, algorithm) gets `arena` directly. A coverage matrix or race gets `shelly-swarm`. A contested design that is costly to reverse gets `architect`, then `interrogate`. Ask `architect` for a checkpoint to see the design before code. Most changes need none of this.

**Build.** Say what you observed and let the playbook demand evidence. Bug: "repro first, then fix and verify". Feature: the behavior plus what must not change. Refactor: "zero behavior change, record output before, prove unchanged after". Perf: the measurement, not a guess. One metric over many attempts: Hillclimb. Ask for the `tdd` skill when a cheap local test path exists. `wizard` when setup needs keys or clicks only you can do. `ticket` with a ticket id drives a Linear ticket to a PR. `typescript-best-practices` applies to `.ts` and `.tsx` files.

**Clean.** Before every PR, the Opening a PR playbook cuts code slop, then runs `unslop` and `no-comments`, in that order. The user does not run them by hand. For work not going through a PR yet, ask for `unslop` on the diff to clean prose and comments, and `no-comments` on the diff to hand comments to Comment Sicko, a reviewer that didn't write them. Pitfall: treating cleanup as optional polish.

**Verify.** Put the finish condition in the first prompt and match the check to the change. CLI: run the command. UI: walk the flow in the running app. Parser or migration: replay saved input. Perf: before and after profiles. Storage: read the value back. `benchmark-checklist` before you report or act on a perf number. `blast-radius` for a small diff you don't trust. `compress-the-clock` when the check would mean waiting hours or days. `create-verification-skill` once, then `maintain-verification-skill` when the feature map drifts. `create-formal-verification-skill` for a race, retry, or state machine tests can't reach. `statechart` to check and draw a TLA+ model. `maintain-formal-verification-skill` when verified code changed without a recheck. Pitfall: accepting "it compiles" or a green build as evidence.

**Ship.** "Use shelly-mode to open the pr" runs cleanup, small ordered commits, evidence in the description, and a body from the `pr` skill. "Use shelly-mode to babysit this pr, get it green" handles conflicts, review threads, then CI. It stops at merge-ready and never merges unless asked. "Use shelly-mode to land the stack" runs per-PR checks, then merges when ready.

**Overnight.** The contract: goal, "done means <checks>", "fresh worktree off <base>", "don't ask me before committing", "keep a decision log", "keep going until done", and a way out. It routes through `figure-it-out` and `show-me-your-work`. In the morning, ask `show-me-your-work` to catch you up on last night, and read the Attention section first. A queue instead of one task: Autopilot-full (merged by morning), Autopilot-stack (one stack, you land it), Orchestrate (multi-day program). Pitfall: a duration is not a finish condition.

**Steer.** Mid-run redirects are one line naming a principle: "apply prove it works, show me the real output". Ask for `bro` when a reply is thorough and you still don't know what it said.

Close calls:

- `how` explains what the code does. `why` explains the reasons. `teach` runs one or both and explains the result plainly.
- `arena` gives every worker the same brief and merges the best parts. `shelly-swarm` splits work into slices or a race and returns one report.
- `interrogate` reviews the diff. `blast-radius` looks for breakage outside the diff and proves the one fact that makes the change safe.
- `recall` rebuilds context across recent chats. `ketchup` covers only this chat since the user's last message. Resuming one chat or branch is the Session pickup playbook.
- `figure-it-out` designs one rigorous run. Orchestrate runs a program across days and many PRs. Autonomous run drives one task to a finish condition.

If a skill under `<SHELLY_ROOT>/skills/` is missing here, read its frontmatter and route by its description. Never name a skill that isn't there. List `<SHELLY_ROOT>/skills/` if unsure. Orchestrate is a shelly-mode playbook, not a skill.

## 5. Playbooks and principles

Playbooks are step lists inside shelly-mode, not skills. Describing the task picks one, and these phrases name one directly:

- "babysit this pr" or "check on pr 123" runs Babysit.
- "land the stack" runs Shipping.
- "take over this branch" runs Session pickup.
- "pause safely" runs Pause safely.
- "full autopilot on this queue" runs Autopilot-full. "autopilot, don't merge" runs Autopilot-stack.
- "run the eval playbook" runs Eval.
- Asking for a plan for multi-phase work runs Multi-phase plan, which writes the plan and doesn't implement it.

The Playbooks section of `<SHELLY_ROOT>/skills/shelly-mode/SKILL.md` lists every playbook, and each one is a file under `<SHELLY_ROOT>/skills/shelly-mode/playbooks/`. Principles are one-rule skills that shelly-mode reads and cites. They live at `<SHELLY_ROOT>/skills/principle-<name>/SKILL.md`. The user steers with their names, as in "apply prove it works. show me the real output."

## 6. Fix a run that went wrong

- The mode stopped applying after a few turns. Start the next task with shelly-mode again.
- A question got treated as the next step of the last task. Say "new task".
- A new model choice had no effect. Check that `~/.config/shelly-stack/models.md` has the line, and that the role name matches one in `<SHELLY_ROOT>/references/runtime.md` exactly.
- Runs cost more than expected. See the cost paragraph in section 2.
- Parallel agents overwrote each other. Give each agent its own worktree.
- An overnight run moved but finished nothing. A long run needs a check that can pass or fail, not a duration.
- The reply claims success from a green build. Ask for the real command, flow, stored value, or profile. That's the prove-it-works principle.
- Agents keep making the same mistake in this repo. Ask for the `correct` skill.

For a run that drifts, [`references/prompting.md`](references/prompting.md) has one-line steers.

## 7. Make shelly-stack my own

- `reflect` after a session turns its lessons into skill edits the user approves.
- `correct` turns repeated corrections into checks that make the mistake impossible.
- "Use shelly-mode to write a skill for <workflow>" runs the authoring playbook, which uses `create-skill`. The Eval playbook tests a skill change blind.
- Fix a misbehaving skill in its own PR, not inside the feature work where it went wrong.

## Reply

Short. In this order:

1. **Answer.** One line. For a stage question, name the stage and why this task is there.
2. **Skills.** Two to four, one line each: name, what it buys for this task, when to skip it.
3. **Your first prompt.** One copyable prompt in a code block, adapted from [`references/recipes.md`](references/recipes.md) and rewritten around their task, with a checkable finish condition. Never a generic example.
4. **Then.** The next stage, one line.
5. **Pitfall.** The one from the stage, one line.
6. **Source.** The absolute local path of the file the answer came from.

Skip lines that don't apply to the question. End by offering to run the first prompt. If they say yes, load that skill and run the prompt. For a shelly-mode prompt, or a task bigger than one stage, load shelly-mode or spawn a helper with the delegate brief.

## Don'ts

- Don't paste a whole skill or playbook. Link it and pull the specific prompt.
- Don't sequence skills for them in the prompt you write. State goal and constraints. That's what shelly-mode routes on.
- Don't invent skills.
