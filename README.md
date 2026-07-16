[中文版](README.zh-CN.md)

When using Codex, we often see it miss things that feel obvious to us: it may run far more tests than necessary or make assumptions about a project that simply do not make sense. Correcting it helps in the current conversation, but that lesson is often forgotten as soon as a new conversation begins. A good harness should keep learning a user's taste, preferences, and working style from these interactions. This Skill does exactly that: it analyzes Codex conversation history, extracts durable preferences, and writes them to project-level or global `AGENTS.md` files, giving Codex a form of continuous learning. You can think of it as a stripped-down version of Hermes. The project intentionally limits itself to preferences suitable for `AGENTS.md` rather than trying to generate Skills. We do not want to lock an agent into particular ways of working, since such constraints can become liabilities as models improve. User preferences, by contrast, are not learned simply by upgrading the model and are therefore worth preserving.

After downloading the Skill, start a separate conversation (or create a dedicated project) and tell Codex, “Use this Skill to optimize my `AGENTS.md`.” Codex will mine your conversation history and present numbered suggestions. Tell it which suggestions you want to accept, and it will apply the corresponding improvements for you. Once the initial review is complete, you can also ask Codex to schedule recurring maintenance that mines new history and proposes incremental improvements.

# Auto-Optimize Codex AGENTS.md

## Features

- Mines active and archived Codex conversations for durable signals: explicit corrections; dissatisfaction that identifies both a problem and an actionable improvement; reusable aesthetic judgments and acceptance criteria; communication and authorization boundaries; and explicit requests to add, change, or remove `AGENTS.md` rules.
- Organizes durable behavioral preferences as project-level or global `AGENTS.md` rules according to where they apply.
- Continues scanning new history after the initial review, processes only records that have not yet been analyzed, and retains candidates that need more evidence so future history can strengthen them.
- Preserves source evidence and generates a complete diff for every suggestion, with support for accepting, editing, rejecting, withdrawing, and restoring learned rules.

## Modes

### Suggest (default)

Suggest mines history and evaluates potential rules, but it only presents numbered suggestions, reasons, and complete diffs; it does not immediately modify the target `AGENTS.md`. You can accept specific numbers in natural language, edit a suggestion, or reject it. Only explicitly accepted suggestions are written. Suggest is recommended for the initial review and whenever you want human oversight.

### Auto (explicit authorization required)

Auto is designed for scheduled incremental maintenance without item-by-item confirmation, and it runs only after you explicitly enable it. It automatically applies only high-confidence rules with a low risk of overconstraining Codex. Anything with insufficient evidence, unclear scope, or elevated risk is left unapplied. For Git projects, Auto can follow your saved preference to commit only the target `AGENTS.md`, without including unrelated repository changes.

## Boundaries and safety

This Skill learns only durable Codex behavioral preferences. It does not export conversations, manage general session history, or generate workflow Skills. It treats only genuine user input and the Assistant's final responses as evidence, preventing injected context, reasoning, tool output, or subagent content from being mistaken for user preferences. When writing, it modifies only its own managed block and preserves the rest of `AGENTS.md`. Project scope is derived only from trusted session metadata, and writes are refused when managed markers are malformed or the target is a symbolic link. Original conversation history always remains read-only.

## Requirements

- Codex with local conversation history under its configured `CODEX_HOME`.
- Python 3.10 or newer.
- Git for project-root discovery and optional commits of accepted changes.

## Install

Install it as a user-scoped Skill:

```bash
git clone https://github.com/ChanTinPing/auto-optimize-codex-agents-md.git ~/.agents/skills/auto-optimize-codex-agents-md
```

Codex normally detects Skill changes automatically. Restart Codex if the Skill does not appear.

## Repository layout

```text
SKILL.md                   Skill workflow and operating boundaries
agents/openai.yaml         Codex UI metadata
references/                Session schema, decision policy, and scheduling guidance
scripts/                   Deterministic scanning, reconciliation, and application tools
```
