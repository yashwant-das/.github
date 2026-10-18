# Adoption checklist

- Choose `small`, `complete`, or `personal` based on the repository's audience and complexity.
- Read existing repository instructions and inventory guides, dependencies, and CI.
- Bring the README into the applicable format and verify its first-run commands.
- Add required guides; consolidate repeated material and update inbound links.
- Register extra maintained guides and their rationale in `.standards.json`.
- Review generated/vendor exclusions; do not exclude active guides to avoid findings.
- Keep source layouts idiomatic. Do not move files without fixing imports and tooling.
- Compare actual runtimes with Python 3.13, Java 21, or Node 24 as applicable.
- Resolve and test compatible stable dependencies; commit locks or pinned declarations.
- Run the local validator and formatting checks before enabling a workflow.
- Publish the central tools first; pin both caller references to its immutable SHA.
- Verify hosted CI, including fork-safe checks, before requiring its status.
- Record exceptions with the rule, reason, validation, owner, and review trigger.

Example minimal `.standards.json` for a starter:

```json
{
  "profile": "small",
  "additional_guides": {},
  "exclude": []
}
```

To use a complete profile, set `profile` to `complete` and provide both required
guides. For personal content use `personal`. Do not copy the central repository's
`standards` profile into an application.
