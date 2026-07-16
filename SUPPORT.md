[中文支持说明](SUPPORT.zh-CN.md)

# Support

Support for Auto-Optimize Codex AGENTS.md is provided on a best-effort basis for the latest version on the `main` branch.

## Before reporting a problem

1. Pull the latest `main` branch and note the commit hash.
2. Confirm Python and Git are available and that Codex can read the repository and the explicitly selected session directories.
3. Reproduce the issue with synthetic or redacted data whenever possible. The fixture generator in [`submission/fixtures`](submission/fixtures/README.md) can help create an isolated starting point.
4. Remove secrets, private source code, full conversation transcripts, usernames, and unnecessary absolute paths from logs and screenshots.

## Request support

Open a [GitHub issue](https://github.com/ChanTinPing/auto-optimize-codex-agents-md/issues) and include:

- the repository commit hash;
- operating system, Python version, and Codex surface;
- the mode used (`Suggest` or explicitly authorized `Auto`);
- minimal reproduction steps;
- expected and actual behavior; and
- redacted error output or a synthetic fixture.

Do not post real transcripts, credentials, API keys, private code, or other confidential information in a public issue.

## Security vulnerabilities

Do not open a public issue for a suspected vulnerability. Report it privately through [GitHub private vulnerability reporting](https://github.com/ChanTinPing/auto-optimize-codex-agents-md/security/advisories/new). See [`SECURITY.md`](SECURITY.md) for scope and reporting guidance.

## Support boundary

This project cannot provide support for OpenAI account access, billing, identity verification, plugin-portal decisions, Codex service availability, or GitHub account administration. Use the relevant provider's official support channel for those matters.

Privacy details are in [`PRIVACY.md`](PRIVACY.md), and usage terms are in [`TERMS.md`](TERMS.md).
