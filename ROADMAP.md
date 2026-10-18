# Roadmap

## Foundation prepared in this release

- Documentation profiles, README boundaries, guide purposes, diagrams, and extra-guide policy.
- Shared folder conventions with language-specific examples.
- Deliberate runtimes and a reproducible dependency/update policy.
- CI/CD requirements, a reusable documentation check, templates, and local checks.

## Adoption next

1. Publish the reviewed foundation and record its immutable commit SHA.
2. Pilot `ai-py-playwright-workbench` as a complete project, preserving its useful
   architecture/development guides and justifying its decisions guide.
3. Pilot `qa-java-selenium` as a starter: consolidate long root guides only where
   useful and preserve its deliberately retained generation prompt as historical context.
4. Tune checks using real pilot findings before adding required status checks.
5. Roll out to the remaining active code repositories in small PRs. Inventory
   existing dependency constraints and CI behavior before upgrading anything.
6. Let Shivani's repositories opt in explicitly; retain their ownership and context.

No consumer repository was modified by this foundation. The validator initially
checks documentation only; source layouts and runtime compatibility need review.

## Later automation

- Reusable Python, Maven, and Node test workflows after pilots reveal common steps.
- Optional external URL/anchor checks, Mermaid rendering, and richer Markdown parsing.
- Dependency/runtime alignment checks with justified compatibility exceptions.
- Drift reporting and an inventory of adopted central revisions.
- Automated artifact/report handling for browser, API, load, and device workflows.

## Broader engineering standards

Coding conventions, review expectations, testing strategy, security and secret
handling, release/versioning policy, observability, AI-agent governance, and deeper
architecture decisions follow demonstrated need. Avoid a large empty taxonomy or
enterprise compliance profiles for this personal repository collection.
