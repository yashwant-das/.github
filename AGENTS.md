# Repository guidance

This repository defines standards for several independent projects. Keep the
foundation small and tailor rules to the existing repository collection.

Read README.md and the relevant maintained guide before changing a standard.
Do not modify sibling repositories, publish changes, or change account settings
as a side effect of editing the standards.

Preserve documentation profiles, deliberate runtime baselines, and justified
exceptions. Add tests for validator behavior changes; human prose needs review,
not tests that assert its exact wording.

Run `npm test`, `npm run lint:docs`, `python3 scripts/validate_docs.py .`, and
`git diff --check` before claiming verification. Do not claim hosted CI success
without an actual run. Historical files under docs/superpowers are implementation
records rather than current user guides.
