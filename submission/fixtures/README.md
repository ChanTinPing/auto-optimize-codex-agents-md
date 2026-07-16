# Synthetic submission fixtures

Generate reviewer fixtures from the repository root:

```bash
python -X utf8 submission/fixtures/create_fixtures.py --output .test-tmp/submission-fixtures
```

The generator creates isolated `CODEX_HOME` trees and disposable Git projects for the cases in [`../TEST_CASES.md`](../TEST_CASES.md). All prompts, answers, identifiers, paths, and repositories are synthetic. The generator reads no normal Codex history, makes no network request, and refuses to overwrite an existing output directory.

Generated fixture data belongs under `.test-tmp/`, which is ignored by Git. Delete it after review if it is no longer needed.
