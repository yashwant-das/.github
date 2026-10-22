# repo-standards

Shared repository standards for documentation, dependencies, structure and quality
gates. AI agents read these documents when
working on any repository that references them.

These standards also apply to repositories owned by Shivani when they choose to
adopt them.

## Scope

This repository is a set of readable instructions for AI agents. It needs no
validator, package tooling, test suite, automated hooks or CI of its own. Review
its content and links when editing. Automated gates in these guides apply to
adopting software repositories; documentation-only repositories need content and
link review. A personal documentation profile does not exempt executable code
from applicable software checks.

This standards repository uses a topic index and focused policy guides instead
of application setup and architecture documents. Its five guides cover separate
policies and the adoption roadmap.

## Requirement levels

- **Required / must:** apply when in scope. Record any exception with its reason,
  owner and review trigger.
- **Default / should / prefer:** use unless an existing approach or project need
  justifies another choice; document the reason.
- **Optional / may:** adopt only when useful to the project.

These describe the target standard. Existing repositories adopt it in stages;
record pending work without claiming full compliance.

## Using the standards

Read the relevant guides before changing a repository. Inspect its existing
structure and commands, apply the relevant profile, and preserve justified
exceptions. Record the chosen profile and a link to these standards in that
repository's README or agent instructions. Use a repository URL that works outside
the local workspace, preferably pinned to the adopted standards revision.

## Standards

- [Documentation](docs/documentation.md) — what every repo should document and how.
- [Folder structure](docs/structure.md) — directory conventions per language stack.
- [Dependencies](docs/dependencies.md) — runtime baselines and dependency practices.
- [CI/CD](docs/cicd.md) — pre-commit gates, required CI checks and workflow safety.
- [Adoption roadmap](docs/adoption.md) — pilot profiles and staged migration.

## License

[MIT](LICENSE)
