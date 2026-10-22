# repo-standards

Shared repository standards for documentation, dependencies, structure and quality
gates. AI agents read these documents when
working on any repository that references them.

These standards apply to Yashwant Das’s repositories and repositories of other
owners who opt in separately.

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

The supported language stacks are Python, Java, JavaScript/TypeScript and Swift.

## Definitions

Pending owner sign-off to adopt this as the shared table; the guides already use these terms,
so treat them as the operative meanings and record any conflict as pending work
until approval.

| Term | Meaning |
| --- | --- |
| Maintained | Intended for current use, with an owner responsible for keeping it accurate or working; excludes archived records and generated output. |
| Complete project | A project assigned the `complete` documentation profile because setup, development and architecture need separate guides. |
| Substantial test framework | Reusable test infrastructure with enough configuration, integrations or execution paths to need development and architecture guides. |
| Maintained framework | Reusable application or testing infrastructure intended for current use and supported by an owner. |
| Software repository | A repository containing executable application, library, test or build/generation code, including personal-content projects with such code. |

## Requirement levels

- **Required / must:** apply when in scope. Record any exception with its reason,
  owner and review trigger.
- **Default / should / prefer / normally:** use unless an existing approach or
  project need justifies another choice; document the reason.
- **Optional / may:** adopt only when useful to the project.

These describe the target standard. Existing repositories adopt it in stages;
record pending work without claiming full compliance. Soft modal phrasing such
as 'normally' or 'usually' reads as a default, not a requirement. Conditional
qualifiers such as 'where practical' or 'where available' are in-scope
conditions, not defaults — the rule applies when the condition holds. Unless
explicitly marked default or optional, policy instructions and rule lists in
these guides are required within scope; examples and rollout suggestions are not
requirements.

## Using the standards

Read the relevant guides before changing a repository. Inspect its existing
structure and commands, apply the relevant profile, and preserve justified
exceptions. Record the chosen profile and a link to these standards in that
repository's README or agent instructions. Use a repository URL that works outside
the local workspace. Adopters should pin the standards to a tag or commit SHA
and record it locally. Use a commit SHA when no suitable tag exists.

## Standards

- [Documentation](docs/documentation.md) — what every repo should document and how.
- [Folder structure](docs/structure.md) — directory conventions per language stack.
- [Dependencies](docs/dependencies.md) — runtime baselines and dependency practices.
- [CI/CD](docs/cicd.md) — pre-commit gates, required CI checks and workflow safety.
- [Adoption roadmap](docs/adoption.md) — pilot profiles and staged migration.

## License

[MIT](LICENSE)
