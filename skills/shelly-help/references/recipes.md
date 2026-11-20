# Prompts worth copying

Swap in the real paths, skills, and done checks. Informal wording works.

## Understand

- `use shelly-mode to read <thread>. restate the underlying issue in your own words, in plain english.`
- `use in-your-own-words on <long or messy ask>`
- `sharpen this prompt: <the prompt you're about to send>`
- `use shelly-mode to investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use how to understand <subsystem>. then use why to find out why it broke recently.`
- `recall my work on <topic> from last week, then read <issue>.`
- `use teach to show me why you implemented it this way and not <other way>. what did you trade off?`
- `use shelly-mode to take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Bug: `use shelly-mode. <symptom>. repro first, then fix and verify.`
- Bug in an app: `use shelly-mode to repro this with the verify-<app> skill. if it repros on main, fix it and show me a video as proof.`
- Bug with a cheap test: `use shelly-mode to repro <bug> first. if there's a cheap test path, tdd it. then fix and rerun.`
- Feature: `use shelly-mode to add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `use shelly-mode to move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `use shelly-mode. <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.` Then ask for the `benchmark-checklist` skill on the numbers.
- Ticket: `use the ticket skill on DEV-123`

## Design and plan

- `use shelly-mode to prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `use shelly-mode. we need <feature>. use architect first, and answer open questions with prototypes. let me review before proceeding.`
- `use shelly-mode to write a tutorial for how i would use <new package> first. then use teach to show me why it beats the current one.`
- `ask arena for a second opinion on this thread and our approach.`
- `use shelly-mode to turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `grill me on this plan` when the open questions are yours to answer.

## Review and ship

- `interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the Dropped list too.
- `what is the blast radius of <change>` for a small diff you don't trust.
- `use create-formal-verification-skill to prove <property> holds in <module>, even when <steps> interleave or retry.` After merges or refactors in that code: ask for the `maintain-formal-verification-skill` skill.
- `use shelly-swarm to check every package under <dir> against its check script. one worker per package. one report.`
- `use shelly-mode to open the pr. small ordered commits, evidence in the description.`
- `use shelly-mode to babysit this pr. get it green.` For status only: `use shelly-mode to check on pr <number>. anything outstanding?`
- `use shelly-mode to land the stack.`

## Away and back

- `use shelly-mode. im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. keep going until done. if you're truly stuck after a few hours, stop and write up why.`
- `use show-me-your-work to catch me up on what you did last night.` Read its Attention section first.
- The `ketchup` skill catches you up on this chat since your last message and lists every call that waits on you. `ketchup-video` does the same as a short video.
- `use shelly-mode. full autopilot on this queue. each item is independent.`
- `use shelly-mode. autopilot these changes, but don't merge. i'll land them.`

## Make it yours

- `reflect. capture what we learned so the next run doesn't repeat it.` Approve only edits that change a future decision.
- Ask for the `correct` skill when agents keep making the same mistake in this repo.
- `bro` restates the last reply in plain words.
