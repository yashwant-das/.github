# Development

## Setup

Use Python 3.13 and Node 24. Clone this repository and work on a topic branch.

```sh
npm ci
```

The formatting runner uses the Markdownlint API and loads only central JSON rules;
consumer JavaScript configuration and inline overrides are not loaded. A temporary
KaTeX 0.18.2 override addresses an upstream low-severity advisory until the math
extension updates its dependency range; a math-syntax regression test covers this
combination. Reassess the override when updating Markdownlint.

The validator uses Python's standard library. Node tooling is for Markdown
formatting; it is installed from `package-lock.json`. There are no runtime services,
credentials, browser downloads, or deployment steps for this repository.

## Checks

Run from the repository root:

```sh
npm test
npm run lint:docs
python3 scripts/validate_docs.py .
git diff --check
```

To check a consumer, pass its directory to the validator. Add its profile config
first; missing configuration fails rather than silently choosing a profile.
The tests create disposable repositories and verify findings and command exits.

## Validator scope

The checker validates profile configuration, required nonempty files, code README
headings and order, registered extra guides, and README discovery links. It checks
relative inline and reference-style Markdown links and images outside fenced code,
including URL-encoded paths. Directory links are accepted. Root-relative links are
resolved from the repository root. Relative links must remain inside that root.

It ignores external schemes, protocol-relative URLs, and anchor-only links. It
does not fetch URLs or validate anchor targets. It supports conventional Markdown
link syntax, not arbitrary embedded HTML/MDX or all nested-parenthesis link forms.
Use angle-bracket destinations for filenames containing parentheses. Plain paths,
inline code, and diagram labels are not treated as links.

Markdownlint performs formatting checks separately. Templates contain replacement
instructions in prose or code fences instead of working-project links. Historical
`docs/superpowers/` artifacts and generated/vendor directories are excluded from
maintained-guide discovery; Markdownlint and link checks use the documented
exclusions. Do not use exclusions to hide active user documentation.

## Troubleshooting

- Missing config: copy a profile example into the consumer's `.standards.json`.
- Additional-guide finding: register a distinct purpose and link the guide directly
  from the README Documentation section, or consolidate redundant guidance.
- Broken file link: check spelling, case on Linux, encoding, and the source file's
  directory. Template destinations should remain inside fenced examples.
- Workflow ref failure: use the published central commit SHA in both caller fields.
- Old runtime: use the declared baseline before reproducing an install failure.

## Updating tools

Update one compatible set at a time. Resolve action SHAs from official release
metadata; update both workflow pins and their release comments. Refresh the dated
library snapshot intentionally. Regenerate the npm lockfile and run all checks.
Test workflow behavior on GitHub after publication; local checks cannot prove a
hosted Actions run or a consumer's repository policy permits the workflow.
