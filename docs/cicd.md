# CI/CD standard

## Pull request baseline

Each code repository MUST have a dependable PR workflow proving its documented
verification commands work. Run Markdown formatting and local-file link checks,
plus applicable formatting, linting, type checks, build, and automated tests. Do
not add a tool solely because another language's repository uses it.

| Project | Normal PR checks | Separate integration checks |
| --- | --- | --- |
| Python framework | Locked install, lint, applicable types, unit tests | Browser/API smoke where available |
| Java framework | Pinned Maven build, applicable static checks, tests | Real service or browser smoke |
| Node test project | `npm ci`, lint/types, tests or spec collection | Actual browser/mobile execution |
| Performance stack | Config checks and a short threshold-gated smoke | Longer load runs, manually or scheduled |
| Device/cloud/local LLM | Static checks and local unit tests | Credentialed/device/model runs |
| Personal content | Applicable documentation/build checks | Deployment only if published |

Spec collection proves discovery, not a working browser flow. Unit tests do not
prove an LLM model or cloud device works. State exactly what runs and what remains
manual. Keep external-target tests separate when the target is unreliable.

## Reusable documentation workflow

Publish this repository before using the example caller in another repository.
The workflow lives at `.github/workflows/documentation.yml`. Copy
[the caller template](../templates/standards-workflow.yml) into the consumer's
`.github/workflows/standards.yml`. Replace both `PUBLISHED_COMMIT_SHA` placeholders
with the same real 40-character commit SHA from this repository.

`standards-ref` is required because a called workflow's ordinary GitHub context
belongs to the caller. The explicit immutable input ensures checkout of central
tools does not accidentally use the consumer's branch or a moving `main`.
Reviewers MUST check that both SHAs match; validation rejects non-SHA inputs but
cannot infer a mismatch with the caller's `uses` reference.

The called workflow checks out the consumer into `repository/`, tools into
`standards-tools/`, runs central Markdownlint using central configuration, and
checks the consumer's `.standards.json` profile. It does not run consumer package
scripts or install consumer dependencies. Caller paths cannot replace central
scripts. A consumer can still change its own configuration; required reviews and
checks are separate governance controls.

Caller repositories need `contents: read` and permission to use the public workflow
and pinned actions. Configure GitHub Actions settings if existing policies restrict
them. No broad token or inherited secrets are needed. This foundation provides a
reusable documentation check, not reusable execution for every test stack.

## Workflow safety and maintenance

- Use `pull_request`, default-branch push, or manual triggers as appropriate.
  Do not execute fork changes with a privileged `pull_request_target` workflow.
- Default to `contents: read`. Give deployment permissions only to deployment jobs.
  Disable persisted checkout credentials when pushes are unnecessary.
- Pin third-party actions to full commit SHAs, with release comments for readability.
  Automated update PRs keep these references current.
- Set job timeouts. Cancel superseded PR runs where this does not disrupt releases.
  Avoid path filters that leave a required check permanently pending.
- Cache dependencies using lockfile keys if useful; do not treat caches as build
  inputs. Install from the committed resolution on every run.
- Upload useful failure reports, traces, and logs with finite retention (normally
  seven days). Redact credentials and personal data before storing artifacts.
- Fork PR checks must work without secrets. Put device/cloud/model tests behind
  separate manual or scheduled workflows and document required secret names.

## Deployment and enforcement

Deploy only projects that need it: portfolio sites, reports, or released packages.
Separate deployment from PR verification. Build a known commit, deploy from the
intended branch/tag, and use an environment with approval where appropriate. Do not
add deployment stages to starter templates without an actual deployment target.

After a pilot succeeds, configure repository rulesets or branch protection to
require dependable check names. Neither publishing `.github` nor adding a workflow
automatically requires its status check. This release does not change settings.

## Inheritance and adoption

GitHub supports certain default community files in a public `.github` repository
when the destination has no corresponding local file. Standards documents, runtime
files, validators, and workflow callers do not automatically inherit. Personal
account defaults apply to that owner's repositories; Shivani's repositories need
explicit adoption and may retain their own contribution guidance.

See GitHub's [default community-file documentation](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
and [reusable workflow documentation](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).
