[中文版](README.zh-CN.md)

Mine local Codex active and archived session history for durable user corrections, dissatisfaction, quality standards, communication preferences, and safety boundaries; then suggest or explicitly auto-apply scoped changes to project-root or global AGENTS.md managed blocks. Use when asked to optimize Codex behavior memory, review or withdraw learned AGENTS.md rules, run incremental daily AGENTS memory maintenance, or configure that maintenance as a scheduled task. Do not use to mine workflow Skills or rewrite unowned AGENTS.md content.

# Auto-Optimize Codex AGENTS.md

## What it does

- Scans active and archived Codex JSONL sessions incrementally.
- Reconstructs genuine user/Assistant turns while excluding injected context, reasoning, tool noise, and delegated subagent sessions.
- Finds durable corrections, acceptance standards, communication preferences, and safety boundaries.
- Produces reviewable, evidence-backed changes for project-root or global `AGENTS.md` files.
- Supports Suggest, confirmed Suggest, and explicitly authorized Auto workflows.

## Safety model

The Skill defaults to Suggest mode and does not change an `AGENTS.md` target until the user accepts a proposal or explicitly enables Auto mode. It writes only inside its managed block, preserves surrounding content, scopes project writes to roots derived from trusted session metadata, and refuses malformed markers or symbolic-link targets. Original session JSONL files are read-only.

## Requirements

- Codex with local session history under its configured `CODEX_HOME`.
- Python 3.10 or newer.
- Git for project-root discovery and optional confirmed-change commits.

## Install

Install it as a user-scoped Skill:

```bash
git clone https://github.com/ChanTinPing/auto-optimize-codex-agents-md.git ~/.agents/skills/auto-optimize-codex-agents-md
```

Codex normally detects Skill changes automatically. Restart Codex if it does not appear.

## Use

Invoke it explicitly:

```text
$auto-optimize-codex-agents-md
```

Example requests:

- “Review my recent Codex sessions and suggest durable `AGENTS.md` improvements.”
- “Show the learned rules and help me withdraw one.”
- “Configure incremental AGENTS memory maintenance as a scheduled task.”

## Repository layout

```text
SKILL.md                   Skill workflow and operating boundary
agents/openai.yaml         Codex UI metadata
references/                Session schema, decision policy, and scheduling guidance
scripts/                   Deterministic scanning, reconciliation, and application tools
```

## Boundaries

This Skill improves durable Codex behavior instructions. It is not a transcript exporter, a general session manager, or a workflow-Skill miner, and it never rewrites unmanaged `AGENTS.md` content.
