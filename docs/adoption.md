# Adoption roadmap

Documentation is the first priority. Adopt these standards in stages, inspecting
the current repository before each change. Record detailed migration status and
verification evidence in that repository's documentation or change description.
Keep private repository details within their existing access boundaries.

## Documentation pilots

| Repository | Proposed profile | First task |
| --- | --- | --- |
| ai-py-playwright-workbench | complete | Retain core guides; distinguish historical plans from current guidance |
| qa-java-playwright | complete | Split the long README into development and architecture guides |
| qa-py-selenium | small | Make the copied template's first successful run explicit |
| yashwant-das.github.io | personal | Explain local build, preview and publishing |

These are proposed targets, not compliance claims. Use the
[documentation profiles](documentation.md) for remaining repositories. Promote
starter/demo profiles when their complexity needs the two core guides. A native
application such as Meters uses `complete`; personal ownership alone does not
make an application a personal-content project. These standards apply to Yashwant
Das’s repositories and repositories of other owners who opt in separately; preserve
their owner-specific workflows.

## Order of adoption

The following order is a default rollout recommendation.

1. Pilot documentation in the four repositories above. Verify that a reader can
   find setup, usage, checks and limitations.
2. Apply the refined documentation conventions to other adopting repositories.
   Preserve useful historical records and personal content.
3. Align folder conventions, runtime declarations, uv/Ruff and dependency practices
   in a separate, tested change per repository. Enable weekly dependency PRs for
   supported ecosystems during this stage, as required by the dependency standard.
4. Apply pre-commit and CI gates to software repositories, documenting required
   checks and integration exceptions. Follow the [scope](../README.md#scope).

Preserve deliberately supported runtime versions until a compatibility review
justifies changing them. Resolve compatible stable library versions during each
upgrade using the dependency standard’s resolution method. Update source paths,
imports, tooling and documentation links together when moving files.

## Completion and later work

For each stage, record the adopted standards revision, profile, pending work,
exceptions and verification evidence in the adopting repository. An exception
needs a reason, owner and review trigger. Check README commands and moved links;
report checks that could not be run. Documentation adoption does not imply
that dependency practices or CI gates have been adopted.

Later work may include shared workflows and coordinated dependency updates across
repositories where reuse reduces maintenance. Per-repository weekly dependency
PRs belong to the adoption stage above; central automation is optional future work.
