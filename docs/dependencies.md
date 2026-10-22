# Dependency standard

## Deliberate runtime baselines

| Runtime | Baseline | How to declare it |
| --- | --- | --- |
| Python | 3.13 | `.python-version`, `requires-python`, and CI |
| Java | 21 | Maven compiler release/toolchain and CI |
| Node.js | 24 | `.node-version` or `.nvmrc`, package engines, and CI |

These are chosen baselines, not claims that no newer runtime exists. Use current
compatible patches within each baseline and coordinate local, CI, and container
versions. A minimum declaration does not prove compatibility with every future
major version. State the versions actually tested. Changes to runtime baselines
need an explicit compatibility review and documentation update.

## Stable library selection

At adoption or an upgrade, resolve the latest stable release compatible with the
chosen runtime and the whole dependency set. Verify against official release notes
or registries, then run relevant checks. Exclude preview, beta, and release-candidate
versions unless a documented project need justifies them. Never use an unbounded
`latest` installation during CI.

Dated reference snapshot, verified from official registries on 2026-10-18:

| Package | Stable version observed | Source |
| --- | --- | --- |
| Python Playwright | 1.64.0 | [PyPI](https://pypi.org/pypi/playwright/json) |
| Node Playwright Test | 1.64.1 | [npm](https://registry.npmjs.org/@playwright%2ftest/latest) |
| Python Selenium | 4.51.0 | [PyPI](https://pypi.org/pypi/selenium/json) |
| Appium server | 3.8.0 | [npm](https://registry.npmjs.org/appium/latest) |

These are reference observations, not a tested universal matrix or forced upgrades.
Selenium Java and other language bindings must be checked in their own registries;
do not infer a binding version from another language. Refresh the snapshot during
adoption if newer releases exist. Existing repository versions have not changed.

## Compatibility sets

- Playwright package versions determine browser binaries. Install browsers from
  the locked package, keep related Node Playwright packages aligned, and match any
  Playwright container image to the package version. Python and Node releases need
  not have identical patch versions when both appear in one project.
- Selenium browser/driver compatibility must be verified. Prefer Selenium Manager
  where supported; document explicit overrides when the environment requires them.
- Appium server, language client, driver, plugins, Android SDK/JDK, Xcode, and device
  OS form a compatibility set. Pin drivers and plugins; check their declared Node,
  npm, Java, and platform requirements before an upgrade. Installing a server alone
  does not prove Android or iOS tests work.
- Native ML packages must be checked against Python, macOS, and Apple Silicon
  support. The runtime baseline does not override unavailable binary support.

## Reproducible installs

- Node: commit the lockfile and use `npm ci` with the supported Node/npm toolchain.
- Python: use uv by default, declare direct dependencies and Python compatibility
  in `pyproject.toml`, commit `uv.lock`, and use `uv sync --locked` in CI. An existing
  fully resolved pinned requirements workflow may remain with a documented reason
  and review trigger; prefer hashes for that install path.
- Java: pin dependencies and build plugins, use Maven dependency management/BOMs
  when appropriate, and pin the wrapper distribution. Use `maven.compiler.release`
  21 for projects targeting Java 21. Maven has no npm-style built-in lockfile.
- Containers: use explicit versions; prefer immutable image digests for published
  or deployment builds. Update the recorded digest intentionally.

Do not document versions in many places manually. Manifests, lockfiles, and runtime
files are the source of truth. Link to them from guides when possible.

## Python quality tools

Use Ruff for linting and formatting. Declare it in a development or lint dependency
group, lock its version, and keep configuration in `pyproject.toml`. Run both
`uv run ruff check .` and `uv run ruff format --check .` after the locked CI install.
Use the same configuration locally and in CI. Match Ruff's target to the lowest
supported Python version, not just the preferred development runtime.

Preserve established rule sets and line lengths unless deliberately migrating.
For a new configuration, start with Ruff's default lint rules plus import sorting
(`I`) and its default formatter. Avoid running overlapping formatters. Ruff does
not replace type checking; maintained Python frameworks should declare a type
checker and its checked scope. Document gradual adoption and exclusions.

## Updates and exceptions

As part of dependency adoption, enable weekly automated dependency PRs for
supported ecosystems. Until adopted, record this as pending work; documentation
adoption alone does not require enabling automation. Group compatible
minor/patch changes when useful. Major updates require explicit review; automation
may propose them but must not merge them blindly. Run the relevant unit, smoke,
build, and integration checks before merging. A skipped device test is not evidence
of mobile compatibility. Prioritize actionable security fixes outside the schedule.

When blocked by upstream compatibility, record the constraint, why the current
version is needed, mitigation, owner, and a review trigger. Avoid broad ignores or
claims of safety based only on a passing package audit.
