# Repository standards foundation

Status: historical implementation design, 2026-10-18. Maintained standards live
in the guides linked from the root README.

## Intent and scope

Create a small central standards repository for Yashwant's existing projects.
Documentation is the first priority, followed by folder conventions, dependencies,
and CI/CD. Other engineering disciplines belong in the roadmap. Shivani's projects
may explicitly adopt the standards; ownership does not change their applicability.
Do not modify other repositories during this release.

The user approved documentation by repository type, justified additional guides,
language-specific layouts, and deliberate runtime baselines. On 2026-10-18 the user
requested continuous execution without further questions. Implement locally on
`standards-foundation`; leave publication and account settings unchanged.

## Documentation contract

Every repository has a meaningful root README. Small utilities, examples, and
starters can keep all essential guidance there. Complete frameworks and
applications require `docs/development.md` and `docs/architecture.md`. Personal
profiles, portfolios, resumes, and notes use a lighter profile. This central
standards repository has its own profile and four maintained standards guides,
plus the development and architecture guides that explain its own implementation.

No numerical cap: an extra guide needs a distinct audience or task, a discoverable
link from the README's documentation index, and no duplicated instructions.
Templates, prompt/task files, vendored agent files, and historical design/plan
artifacts are not maintained user guides. Historical artifacts must be labeled.
Use sentence-case headings, fenced commands with language labels, relative local
links, and Mermaid when a diagram clarifies relationships or flow. Avoid badges
that duplicate static version declarations.

## Structure and dependency contract

Use `docs/`, `docs/assets/`, `scripts/`, and `.github/workflows/` by purpose, creating
folders only when used. Python packages use `src/<package>/` and `tests/`; Java uses
Maven conventions; Node projects use layouts matching their application or test
purpose. Preserve justified exceptions and migrate incrementally.

Runtime baselines are Python 3.13, Java 21, and Node 24. They are deliberate
baselines, not floating latest releases. Library baselines are latest compatible
stable releases at adoption time, verified against official registries and tested
as a compatible set. Record a dated reference snapshot, not a promise of permanent
currency. Lock dependencies; CI installs the recorded resolution. Update PRs run
the relevant tests; major updates get explicit review. Appium server, clients,
drivers, plugins, SDKs, and browser binaries need compatibility checks.

## Enforcement architecture

Four standards guides define documentation, structure, dependencies, and CI/CD.
Templates demonstrate adoption. A Python standard-library validator checks an
explicit `.standards.json` profile, required nonempty documents, mandatory README
headings for code profiles, discoverability of maintained guides, and relative
inline/reference Markdown file links and images outside fenced code. It reports
actionable errors and returns nonzero on violations. Missing configuration and
unknown profiles fail closed. Directory links are valid. External URLs and heading
anchors are outside this initial check; do not claim those are checked.

The Markdownlint API handles formatting with central JSON rules. A reusable documentation workflow checks out the
caller and the standards tools at the called workflow's immutable revision into
separate paths. It installs central tooling from its lockfile and does not execute
caller scripts. A thin caller workflow and explicit adoption enable reuse. Pin
third-party actions to full SHAs, disable persisted checkout credentials, use
read-only tokens, timeouts, and ordinary pull_request events. A self CI workflow
also runs validator regression tests. Other stack-specific CI examples are
documented recipes, not universal command runners.

## GitHub behavior and rollout

Central documentation and workflows do not automatically apply to other repos.
Only supported community defaults inherit within the same owning account when no
local override exists. Ship a broadly applicable CONTRIBUTING default and PR
template; omit account-wide security/support promises and organizational profile
files. Shivani's repositories explicitly call the workflow and adopt the guides.
Required checks/rulesets and publishing remain explicit later actions.

Publish the central commit before adding caller workflows. Pin callers to the
published full commit SHA. Validate locally, then pilot a complete framework and
a starter before wider adoption. Record justified exceptions with rationale,
affected rule, validation, owner, and review trigger.

## Acceptance and limits

- Standards and templates explain all four agreed focus areas.
- The central repository validates itself and all regression tests pass.
- Tests exercise passing profiles, missing/empty files, malformed configuration,
  README headings, guide discovery, local links, fences, exclusions, and CLI exits.
- CI syntax and action revisions are verified locally where tools permit.
- No dependency installation or migration occurs in any existing project.
- No push, release, ruleset change, or claim of hosted CI success occurs locally.
- A roadmap identifies stack workflows, a pilot, and later engineering standards.
