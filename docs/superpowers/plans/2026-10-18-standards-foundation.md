# Repository standards foundation implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan
> task by task in the current session. User requested execution without more questions.

**Goal:** Deliver reviewable standards, templates, and executable documentation checks.

**Architecture:** Human standards live in four guides; an explicit profile drives
a local Python validator. Locked Markdown tooling and a reusable workflow enforce
the objective subset without running caller-provided commands.

**Tech stack:** Python 3.13 standard library, Node 24, Markdownlint API, GitHub Actions.

**Spec:** [Design](../specs/2026-10-18-standards-foundation-design.md).

## Global constraints

- Python 3.13, Java 21, Node 24 remain deliberate runtime baselines.
- Work only in the newly cloned `.github` repository on `standards-foundation`.
- No publishing, consumer migrations, or account settings changes.
- Maintained guides have no arbitrary count limit; additional guides need justification.
- Tool snapshots cite official release sources and the verification date.
- External URL status and heading anchors are not part of the initial link check.

## Review focus

- Missing or invalid profiles must fail rather than silently pass.
- Fenced example links and template placeholders must not cause false failures.
- Relative paths, reference links, images, and URL-encoded filenames must be checked.
- Generated/vendor documentation must not overwhelm maintained-guide checks.
- A reused workflow must use its own revision for tools, not the caller revision.

## Task 1: Standards and adoption materials

**Files:** `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `docs/*.md`,
`templates/*.md`, `templates/standards-workflow.yml`, `.standards.json`,
`AGENTS.md`, `.github/PULL_REQUEST_TEMPLATE.md`.

**Interfaces:** Produces profile names `small`, `complete`, `personal`, `standards`;
configuration keys `profile`, `exclude`, `additional_guides`.

- [x] Write the four standards and the central development/architecture guides.
- [x] Add templates and a checklist describing explicit repository adoption.
- [x] Review prose against the design and all agreed decisions; check links after Task 2.

## Task 2: Documentation validator

**Files:** `tests/test_validate_docs.py`, `scripts/validate_docs.py`.

**Interfaces:** `validate(root: Path) -> list[str]`; command
`python3 scripts/validate_docs.py [repository]` returns 0 on success, 1 on violations.

- [x] Write real temporary-repository fixtures covering all four profiles and the
  five review-focus failure modes; assert findings and process exit codes.
- [x] Run `python3 -m unittest discover -s tests -v`; verify failure before implementation.
- [x] Implement profile/schema validation, required documents, guide discovery,
  local inline/reference file links, and generated/vendor exclusions.
- [x] Run the full suite and the validator on this repository; expect all passing.

## Task 3: Formatting and reusable CI

**Files:** `package.json`, `package-lock.json`, `.markdownlint.json`,
`.github/workflows/ci.yml`, `.github/workflows/documentation.yml`,
`.github/dependabot.yml`, `.gitignore`, `.editorconfig`, `.python-version`, `.node-version`.

**Interfaces:** `npm run lint:docs`, `npm test`; reusable workflow takes no arbitrary
commands, checks the caller, and loads tools using the explicit immutable
`standards-ref` input matching the caller's workflow reference.

- [x] Resolve immutable action SHAs and lock the Markdown tool dependency.
- [x] Verify how to obtain the called workflow revision; record any simplification.
- [x] Implement reusable and self CI with read-only permissions and timeouts.
- [x] Run full tests, Markdown lint, validator, workflow syntax checks, and
  `git diff --check`; review limitations and caller template instructions.
- [x] Update this checklist and commit the locally verified result.

## Execution record

Historical execution record: implementation and final verification completed locally.

Ruling: use an explicit required `standards-ref` full SHA input, duplicated with
caller `uses`, instead of OIDC revision discovery. This keeps token permissions
read-only and avoids an authentication dependency; reviewers must verify both refs
match. Use the Markdownlint API with a central config so consumer JS configuration
cannot execute as a side effect of formatting.


- Task 1: complete. Four standards, central guides, templates, roadmap, and explicit
  adoption instructions are present; other repositories remain unchanged.
- Task 2: complete. Tests were observed failing before implementation. The final
  suite contains 22 tests, including CLI, reference discovery, and central lint
  isolation. All pass on Python 3.13.16 and Node 24.21.0.
- Task 3: complete. A locked clean install succeeds. Markdown formatting passes for
  15 active Markdown files; central documentation validation passes. Actionlint
  1.7.12 validates both executable workflows. npm reports zero known vulnerabilities
  in the resolved dependency tree. Staged whitespace checks pass.
- Independent review found that reference definitions could falsely satisfy guide
  discovery. Fixed by counting actual usages separately; a regression covers a
  reference used only outside Documentation.
- Ruling: the latest Markdownlint API returns a structured map, so explicitly format
  its findings rather than relying on legacy string conversion.
- Ruling: temporarily override KaTeX to patched 0.18.2; test math syntax and reassess
  with upstream updates. No downgrade or blind forced audit fix was used.
- Ruling: preserve this dedicated new clone and local topic branch rather than
  creating an additional worktree for an empty repository.
- Publication and hosted CI have not run. Caller placeholders must be replaced with
  the published central SHA; no consumer or account settings were changed.
