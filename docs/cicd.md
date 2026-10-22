# CI/CD

Required checks and workflow safety for repositories that follow these
standards.

## PR check baselines

Apply the [scope](../README.md#scope) first. For software repositories, combine
checks for every supported language used with the relevant project-specific checks
below. Use the shared [definitions](../README.md#definitions).
Documentation profiles do not replace these requirements.

| Language / files | Required PR checks |
| --- | --- |
| Python | Ruff lint and format, tests; type check for maintained frameworks |
| Java | compile, tests, static analysis |
| JavaScript / TypeScript | lint, format check, tests; type check for TypeScript |
| Swift | native build and applicable tests/checks, documented per repository |
| Maintained Markdown | markdownlint-cli2 with the [documentation baseline](documentation.md) |

| Project purpose | Additional checks / evidence |
| --- | --- |
| Browser / API / database | Controlled integration or smoke tests for supported flows |
| Performance / monitoring | Load configuration and threshold checks; document full-run scope |
| Device / cloud / LLM | Document integration prerequisites, execution evidence and skipped scope |
| Personal content with executable code | Applicable build or generation checks plus content/link review |

Include Markdown linting on documentation-only PRs in software repositories.
Tests must exercise meaningful behavior; do not create empty suites to satisfy
a row. Document unavailable or inapplicable checks as exceptions.

State in the development guide (or README for small projects) what checks cover.
An agent-driven test project may use spec collection as a documented exception
when execution requires an interactive agent. Collection proves discovery only.

## Pre-commit gates

Adopting software repositories must provide fast checks on staged files before
commit. Use [pre-commit](https://pre-commit.com/) by default, configured in
`.pre-commit-config.yaml`. Preserve an established hook manager when it provides
the same checks; avoid installing competing managers. Applicability follows the
[scope](../README.md#scope).

| Files | Required checks |
| --- | --- |
| Maintained Markdown | markdownlint-cli2 with the documentation baseline |
| Python | Ruff lint and format checks |
| JavaScript / TypeScript | Established linter and formatter in check mode |
| Java | Established formatter/style check when practical on staged files |
| Applicable text/config files | Trailing whitespace, final newline, merge-conflict markers, YAML/JSON syntax |

Use file filters and narrow exclusions for generated files and dependencies.
Preserve intentional Markdown hard breaks; configure syntax checks for actual
file formats (for example, JSONC is not strict JSON). Document exceptions.

Pin hook revisions and tool versions, aligning them with CI and project locks.
Document installation after cloning: `pre-commit install`, or the existing hook
manager's equivalent. For uv projects, lock pre-commit in the development group
and use `uv run pre-commit install`. Document `pre-commit run --all-files` for
initial adoption and full checks, using `uv run` when project-managed.

Keep commit checks fast and independent of services or credentials after tool
setup. Leave full test suites, builds, type checks and browser/device/cloud runs
in CI or an optional pre-push stage. If a hook changes files, review and restage
them before retrying; do not automatically stage unrelated changes.

A failed applicable hook blocks the local commit. Agents must not bypass hooks
without explicit user authorization; record any authorized bypass and unresolved
checks. Hooks can be skipped or absent, so CI must independently enforce the
required checks with the same rules and versions. Hooks check staged files; CI
runs lint and format checks across all maintained files in scope, including files
unchanged by the PR. Apply documented exclusions consistently in both.

## Quality gates

The following gates are required within scope.

- Identify required check names and configure branch protection or rulesets where
  available. Workflow presence alone does not make a check required for merging.
- Required checks must pass for the revision being merged. Do not mask failures
  with `continue-on-error`, unconditional success, or empty test runs.
- Keep offline checks runnable without secrets. Run browser/API smoke tests against
  controlled targets where practical; starter templates must demonstrate a working
  example from a clean checkout.
- Separate device, paid cloud and LLM integration checks. Document how to run them,
  their prerequisites and when they are required. A skipped run is not a pass;
  changes to those integrations need relevant execution evidence or a recorded
  exception with owner, reason and review trigger.
- Preserve existing coverage thresholds. Choose new thresholds from meaningful
  project risks and measured coverage; there is no universal percentage quota.
- Run the same documented commands locally and in CI. Changes to documentation
  need Markdown linting where required above and a content/link review, not a new
  test suite.

## Workflow safety

The following workflow rules are required.

- Pin every third-party action to a full commit SHA.
- Use `pull_request`, not `pull_request_target`, for PR-triggered workflows.
- Set `permissions` to the minimum required (usually `contents: read`).
- Add `timeout-minutes` to every job.
- Cache dependency installs when the project has a lock file.
- Set `persist-credentials: false` on checkout steps.
- Keep artifact retention short (1–3 days for CI; longer only for releases).

## Deployments

Deploy the checked revision after required checks pass, from a trusted branch
or release event. Keep deployment credentials out of untrusted PR jobs. Define
environments in GitHub when the project has staging or production targets.

## GitHub inheritance

GitHub provides defaults only for supported community health files from a public
`.github` repository in the same account. These standards, `AGENTS.md` and
workflows do not automatically propagate. Each adopting repository must reference
the standards explicitly. They apply to Yashwant Das’s repositories and
repositories of other owners who opt in separately.
See [GitHub's supported defaults](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
