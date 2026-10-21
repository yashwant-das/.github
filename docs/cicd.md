# CI/CD

Required checks and workflow safety for repositories that follow these
standards.

## PR check baselines

Every repository must run checks on pull requests before merging:

| Project type | Checks |
| --- | --- |
| Python framework | lint, unit tests, type check |
| Java framework | compile, unit tests, static analysis |
| Node test project | lint, tests or spec collection |
| Performance / monitoring | lint, unit tests |
| Device / cloud / LLM | lint, unit tests, note integration scope |
| Personal content | lint (if applicable), link check |

State in the development guide what the checks cover and what they do not
(e.g., spec collection proves discovery, not a working browser flow).

## Workflow safety

- Pin every third-party action to a full commit SHA.
- Use `pull_request`, not `pull_request_target`, for PR-triggered workflows.
- Set `permissions` to the minimum required (usually `contents: read`).
- Add `timeout-minutes` to every job.
- Cache dependency installs when the project has a lock file.
- Set `persist-credentials: false` on checkout steps.
- Keep artifact retention short (1–3 days for CI; longer only for releases).

## Deployments

Deploy after checks pass. Define environments in GitHub when the project has
staging or production targets.

## GitHub inheritance

GitHub applies files from a `.github` repository to other repositories in the
same account as defaults. Repositories owned by Shivani must opt in explicitly;
GitHub inheritance does not cross account boundaries.
