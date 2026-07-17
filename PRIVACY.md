# Privacy Policy

**Effective date:** July 16, 2026

This Privacy Policy describes how Auto Preference Learner (the “Skill”), published and maintained by ChanTinPing (the “Publisher”), handles data. It applies to the Skill's bundled instructions and scripts and to Publisher-maintained support channels. OpenAI, GitHub, Git, operating systems, and other services have their own terms and privacy practices.

## Summary

The Publisher operates no backend for this Skill and does not automatically receive your Codex history, optimizer artifacts, or learned rules. The bundled Python scripts contain no HTTP client, telemetry, analytics, advertising, or direct upload functionality. The Skill does, however, read and copy selected local conversation content into local working and state files, and Codex may process content placed in its context under your OpenAI product, account, workspace, and data-control settings.

## Data the Skill processes

Depending on the workflow, the Skill may read or process:

- active and archived Codex session JSONL, including user inputs and Assistant final answers;
- session, thread, turn, and record identifiers; timestamps; active/archive state; source paths; line and byte positions; CWDs; and inferred project roots;
- event structure used to identify genuine user turns, completed answers, injected context, and delegated subagent sessions;
- on-demand evidence slices containing user or Assistant messages, lifecycle events, or summaries of tool names, arguments, inputs, or outputs;
- token quota and rate-limit observations used by the scheduled-run preflight;
- existing project and global `AGENTS.md` content;
- optimizer state, prior decisions, rejected candidates, tombstones, reports, and cursors; and
- local Git status, index metadata, repository roots, and commit identifiers.

Tool summaries and conversation content may contain source code, file contents, personal information, credentials, or secrets. The evidence helper limits event types and length but does not detect or redact sensitive content.

## Purposes

The Skill uses this data to reconstruct completed conversations, identify durable working preferences, determine project or global scope, produce evidence-backed proposals and diffs, prevent duplicate or withdrawn rules from reappearing, apply authorized managed-block changes, and maintain incremental checkpoints.

## Local storage and changes

The documented workflow stores plaintext artifacts under `$CODEX_HOME/auto-preference-learner/`, including timestamped runs, scan manifests, batches, review chunks, optional evidence, decisions, plans, `state.json`, `decisions.jsonl`, reports, and a lock file. These files may contain full selected user inputs and Assistant final answers, absolute paths, proposed rules, evidence references, diffs, and Git commit IDs. The Skill does not provide application-level encryption.

Suggest mode does not modify target `AGENTS.md` files, but it does write optimizer state, audit, report, and run artifacts. Confirmed Suggest and explicitly authorized Auto workflows can create or modify the managed block in an authorized project-root or global `AGENTS.md`. Depending on mode and saved preference, the Skill can create a local Git commit containing only the target `AGENTS.md`; it does not run `git push`. User-configured Git hooks or signing helpers may have effects outside the Skill's control.

Original Codex session JSONL is opened read-only by the bundled scripts and is not edited or deleted.

## Network processing and third parties

The bundled scripts do not directly transmit data over a network, and the Publisher has no service that receives runtime data. This does not mean the complete workflow is offline: content reviewed by Codex may be processed by OpenAI under the terms and data controls applicable to your account or workspace. Scheduled-task definitions and run metadata may be handled by the Codex scheduling surface. GitHub processes repository visits, issues, security reports, and other support activity under GitHub's policies.

## Retention and deletion

The Skill has no automatic expiry, log rotation, or secure-erasure feature. Local run artifacts, state, reports, audit entries, and copied conversation text remain until you remove them or an external cleanup process does so. Rejecting a suggestion or withdrawing a rule does not erase related audit entries, reports, tombstones, run files, or Git history.

To remove locally retained optimizer data, disable any related scheduled task separately, remove any learned rules you no longer want, and remove the optimizer directory at `$CODEX_HOME/auto-preference-learner/`. Removing this directory deletes checkpoints and may cause remaining source sessions to be processed again. Local Git commits and any remotely pushed history must be managed separately. Deleting an original Codex session does not automatically delete text already copied into optimizer artifacts.

## Data received through support

If you open a GitHub issue or otherwise contact the Publisher, the Publisher receives the information you choose to submit. Do not include raw session transcripts, credentials, secrets, personal data, or unredacted absolute paths in public issues. Security-sensitive reports should use the private channel described in [SECURITY.md](SECURITY.md).

## Security

The Skill uses scoped paths, managed-block writes, atomic local files, evidence bounds, and explicit authorization gates to reduce risk, but no software is guaranteed secure. You are responsible for filesystem permissions, device security, backups, OpenAI data controls, Git configuration, and reviewing changes before acceptance.

## Changes and contact

This policy may be updated when the Skill's behavior or submission requirements change. Material changes will be published in this repository. For privacy questions, use the private security-reporting channel or the options in [SUPPORT.md](SUPPORT.md).
