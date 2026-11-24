"""Fail when a skill or reference names one client's tools, agent types, models, or paths.

references/runtime.md maps client tools, README.md gives per-client install steps, and agents/shelly-agent.md is a client agent file, so all three may name clients. evals/ holds Claude Code eval cases and is skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {ROOT / "references/runtime.md", ROOT / "README.md", ROOT / "agents/shelly-agent.md"}
BANNED = [
    (r"subagent_type", "agent type: name a role and a brief instead"),
    (r"\bSkill tool\b|`Skill`", "Skill tool: say 'load the <name> skill'"),
    (r"\bAgent tool\b|`Agent`|\bAgent call", "Agent tool: say 'spawn a helper'"),
    (r"\bSendMessage\b|\bTeamCreate\b|\bTaskCreate\b|\bTodoWrite\b", "Claude Code tool"),
    (r"\bToolSearch\b", "ToolSearch: Claude Code only"),
    (r"`Workflow`|\bWorkflow tool\b", "Workflow tool: use async spawns per runtime.md"),
    (r"\bAskUserQuestion\b", "AskUserQuestion: say 'ask the user'"),
    (r"\bScheduleWakeup\b|`Monitor`|\bMonitor tool\b", "Claude Code wait tool"),
    (r"CLAUDE_PLUGIN_ROOT", "use <SHELLY_ROOT>"),
    (r"~/\.claude/|~/\.codex/", "client config path"),
    (r"\bshelly-stack:[a-z]", "client skill prefix: use the bare skill name"),
    (r"\$shelly-stack|\$[a-z]+-[a-z-]+ skill", "Codex skill syntax"),
    (r"(?<![\w/.-])/(shelly-mode|shelly-help|setup-shelly-stack|swarm|arena|architect|interrogate|how|why|reflect|recall|ticket|bro|teach|ketchup|ketchup-video|sharpen|tdd|wizard|statechart|correct|no-comments|figure-it-out|grilling|unslop|loop|goal|code-review|create-skill|create-verification-skill|maintain-verification-skill|untangle-codebase|show-me-your-work|compress-the-clock|in-your-own-words|benchmark-checklist|blast-radius|pr|create-formal-verification-skill|maintain-formal-verification-skill)\b", "slash command: name the skill"),
    (r"\b(general-purpose|codex:codex-rescue|shelly-reader|shelly-agent|shelly-(opus|sonnet|fable)-\w+)\b", "client agent type"),
    (r"\bclaude-(opus|sonnet|fable|haiku)\b|\b(opus|sonnet|fable|haiku|Opus|Sonnet|Fable|Haiku)\b", "model name: name a role"),
    (r"\bClaude Code\b", "client name"),
]


def main() -> int:
    bad = 0
    for path in sorted(ROOT.rglob("*.md")):
        if path in ALLOWED or ".git" in path.parts or path.relative_to(ROOT).parts[0] == "evals":
            continue
        for n, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if "http://" in line or "https://" in line:
                line = re.sub(r"https?://\S+", "", line)
            for pattern, why in BANNED:
                if re.search(pattern, line):
                    print(f"{path.relative_to(ROOT)}:{n}: {why}: {line.strip()[:140]}")
                    bad += 1
                    break
    print(f"{bad} findings")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
