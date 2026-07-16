# Security Policy

## Supported version

Security fixes are provided on a best-effort basis for the latest version on the `main` branch.

## Reporting a vulnerability

Report suspected vulnerabilities privately through [GitHub private vulnerability reporting](https://github.com/ChanTinPing/auto-optimize-codex-agents-md/security/advisories/new). Do not open a public issue before a fix or coordinated disclosure is available.

Include the affected commit, impact, minimal reproduction steps, and a synthetic proof of concept where possible. Share the least sensitive information necessary. Do not include real conversation transcripts, credentials, API keys, private source code, or unrelated personal data.

Relevant reports include unintended path access, writes outside the managed `AGENTS.md` block, evidence-boundary bypass, prompt-injection or delegated-session misclassification, rollback or withdrawal failures, and accidental disclosure of locally stored review artifacts.

Problems in Codex, Git, Python, the operating system, or another third-party service should normally be reported to that provider unless this repository's code creates or materially worsens the issue.

For non-security help, see [`SUPPORT.md`](SUPPORT.md).
