#!/usr/bin/env python3
"""Offline self-check for the AGENTS.md commit path.

Usage:
    python3 -X utf8 scripts/selftest.py

Creates throwaway Git repositories in a temp dir and asserts that
commit_agents commits a tracked AGENTS.md, skips an ignored one, and
refuses a target outside the repository.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from apply_agents_update import commit_agents
from apply_agents_update import validate_application
from prepare_review_chunks import review_chunks
from reconcile_agents import reconcile


def make_repo(base: Path, gitignore: str = "") -> Path:
    repo = base / "repo"
    repo.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "tester"], check=True)
    if gitignore:
        (repo / ".gitignore").write_text(gitignore, encoding="utf-8")
    return repo


def log(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "log", "--oneline"], capture_output=True, text=True, check=False
    )
    return result.stdout.strip()


def case_tracked_commits() -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(Path(tmp), "*.pyc\n")
        target = repo / "AGENTS.md"
        target.write_text("first\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "--", "AGENTS.md"], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "init"], check=True)
        target.write_text("second\n", encoding="utf-8")
        result = commit_agents(repo, target)
        if result.get("committed") is not True:
            return f"tracked AGENTS.md should commit, got {result}"
        if "chore: update learned Codex preferences" not in log(repo):
            return f"expected the preference commit in history, got {log(repo)!r}"
    return None


def case_ignored_is_skipped() -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(Path(tmp), "AGENTS.md\n")
        target = repo / "AGENTS.md"
        target.write_text("content\n", encoding="utf-8")
        result = commit_agents(repo, target)
        if result.get("committed") is not False:
            return f"ignored AGENTS.md should not commit, got {result}"
        if "gitignore" not in str(result.get("reason", "")):
            return f"expected a gitignore reason, got {result}"
        if log(repo):
            return f"ignored AGENTS.md should leave history empty, got {log(repo)!r}"
    return None


def case_outside_repo_refused() -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        repo = make_repo(base)
        outside = base / "outside.md"
        outside.write_text("content\n", encoding="utf-8")
        result = commit_agents(repo, outside)
        if result.get("committed") is not False:
            return f"outside target should not commit, got {result}"
    return None


def case_oversized_record_is_trimmed() -> str | None:
    batch = {
        "records": [
            {"record_id": "R-big", "project_root": "/tmp/p", "text": "x" * 200},
            {"record_id": "R-small", "project_root": "/tmp/p", "text": "y" * 10},
        ],
        "feedback_episode_candidates": [
            {"record_ids": ["R-big"], "context_records": [{"record_id": "R-old", "text": "z" * 4000}]}
        ],
    }
    chunks, warnings = review_chunks(batch, max_records=100, max_chars=1500)
    covered = {record_id for chunk in chunks for record_id in chunk["record_ids"]}
    if covered != {"R-big", "R-small"}:
        return f"every record should survive, got {sorted(covered)}"
    if len(warnings) != 1 or warnings[0].get("record_id") != "R-big":
        return f"expected one warning for R-big, got {warnings}"
    trimmed = [chunk for chunk in chunks if chunk["record_ids"] == ["R-big"]]
    if not trimmed:
        return "the oversized record should get its own chunk"
    if any(episode.get("context_records") for episode in trimmed[0].get("feedback_episode_candidates", [])):
        return "episode context should be dropped for the trimmed record"
    return None


def case_handwritten_rule_is_noop() -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        (home / "AGENTS.md").write_text("# 我的规则\n\n- 先跑测试再改代码\n", encoding="utf-8")
        decisions = [
            {
                "action": "add",
                "target": "global",
                "instruction": "先跑测试再改代码",
                "evidence_refs": ["R-1"],
                "explanation": "candidate rule",
            }
        ]
        batch = {
            "record_ids": ["R-1"],
            "records": [{"record_id": "R-1", "project_root": str(home / "proj")}],
            "allowed_project_roots": [],
        }
        plan = reconcile(decisions, batch, home, "suggest", {})
        decision = plan["decisions"][0]
        if decision.get("action") != "no-op":
            return f"a rule the user already wrote should be a no-op, got {decision}"
        if plan["targets"]:
            return f"nothing should change on disk, got {plan['targets']}"
    return None


def case_global_rule_converges_project_copy() -> str | None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        home = base / "home"
        project = base / "proj"
        home.mkdir()
        project.mkdir()
        (home / "AGENTS.md").write_text("# 全局规则\n", encoding="utf-8")
        (project / "AGENTS.md").write_text(
            "<!-- auto-preference-learner:start -->\n"
            "## Learned working preferences\n"
            "\n"
            "- 先跑测试再改代码\n"
            "<!-- auto-preference-learner:end -->\n",
            encoding="utf-8",
        )
        decisions = [
            {
                "action": "add",
                "target": "global",
                "instruction": "先跑测试再改代码",
                "evidence_refs": ["R-1"],
                "explanation": "promoted to a global rule",
            }
        ]
        batch = {
            "record_ids": ["R-1"],
            "records": [{"record_id": "R-1", "project_root": str(project)}],
            "allowed_project_roots": [str(project)],
        }
        plan = reconcile(decisions, batch, home, "suggest", {})
        removals = [item for item in plan["decisions"] if item.get("action") == "remove"]
        if len(removals) != 1:
            return f"expected one project removal, got {plan['decisions']}"
        removal = removals[0]
        if Path(str(removal.get("project_root"))).resolve() != project.resolve():
            return f"the removal should target the project root, got {removal}"
        if removal.get("existing_instruction") != "先跑测试再改代码":
            return f"the removal should quote the existing rule, got {removal}"
        project_target = [
            item for item in plan["targets"] if Path(item["path"]).resolve() == (project / "AGENTS.md").resolve()
        ]
        if not project_target:
            return f"the project file should appear in the plan, got {plan['targets']}"
        removed = [
            line
            for line in project_target[0]["diff"].splitlines()
            if line.startswith("-") and not line.startswith("---")
        ]
        if not any("先跑测试再改代码" in line for line in removed):
            return f"the project diff should remove the duplicate rule, got {project_target[0]['diff']}"
    return None


def case_deduped_rule_does_not_block_apply() -> str | None:
    """A rule the user already has becomes a no-op; its cross-project evidence must not block apply."""
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        home = base / "home"
        project_a = base / "proj_a"
        project_b = base / "proj_b"
        for path in (home, project_a, project_b):
            path.mkdir()
        (home / "AGENTS.md").write_text(
            "<!-- auto-preference-learner:start -->\n"
            "## Learned working preferences\n"
            "\n"
            "- 先跑测试再改代码\n"
            "<!-- auto-preference-learner:end -->\n",
            encoding="utf-8",
        )
        batch = {
            "codex_home": str(home),
            "record_ids": ["R-1", "R-2"],
            "records": [
                {"record_id": "R-1", "project_root": str(project_a)},
                {"record_id": "R-2", "project_root": str(project_b)},
            ],
            "allowed_project_roots": [str(project_a), str(project_b)],
            "explicit_project_roots": [],
        }
        decisions = [
            {
                "action": "add",
                "target": "global",
                "instruction": "先跑测试再改代码",
                "evidence_refs": ["R-1", "R-2"],
                "explanation": "两个项目都出现过",
            }
        ]
        plan = reconcile(decisions, batch, home, "suggest", {})
        if plan.get("errors"):
            return f"plan should reconcile cleanly, got {plan['errors']}"
        decision = plan["decisions"][0]
        if decision.get("action") != "no-op":
            return f"the already-covered rule should become a no-op, got {decision}"
        if not decision.get("neutralized_by_existing_rule"):
            return f"the no-op should be flagged as neutralized, got {decision}"
        error = validate_application(plan, "suggest", None, set(), False, batch)
        if error:
            return f"apply should accept the plan, got: {error}"
    return None


def main() -> int:
    cases = [
        ("tracked AGENTS.md commits", case_tracked_commits),
        ("ignored AGENTS.md is skipped", case_ignored_is_skipped),
        ("target outside repo is refused", case_outside_repo_refused),
        ("oversized record is trimmed, not fatal", case_oversized_record_is_trimmed),
        ("rule the user already wrote is a no-op", case_handwritten_rule_is_noop),
        ("global rule converges the project copy", case_global_rule_converges_project_copy),
        ("deduped rule does not block apply", case_deduped_rule_does_not_block_apply),
    ]
    failures = []
    for name, case in cases:
        problem = case()
        if problem:
            failures.append(f"FAIL {name}: {problem}")
        else:
            print(f"ok   {name}")
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        return 1
    print(f"{len(cases)} 项自检全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
