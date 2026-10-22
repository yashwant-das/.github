# Documentation standard

Keep documentation useful to readers and AI agents. Choose a profile based on
what the repository does, and record it in its README or agent instructions.
Use the shared [definitions](../README.md#definitions). Instructions below are
required unless explicitly marked default or optional.

## Profiles and document budget

| Profile | Required documents | Use for |
| --- | --- | --- |
| `small` | README | Focused demos and simple starter templates |
| `complete` | README, development guide, architecture guide | Maintained applications and substantial test frameworks |
| `personal` | README, with headings suited to the content | Profiles, portfolios, resumes and reference notes |

A complete project normally has two core guides and at most two additional
maintained guides. Add more only when the README documentation index explains
why each is needed. Small and personal projects may add focused guides when
useful; promote small projects when setup or architecture needs sustained detail.
Do not create empty guides to satisfy a count.

The budget excludes community files, generated references, changelogs and
historical plans. Reference notes that are the repository's main content are
also excluded. Keep records in existing historical plan directories clearly
labelled as historical. They are not current setup guides.

## Root README

Start with the project name and a short explanation of purpose, intended user,
status (demo, starter or maintained project), scope and important limitations.
For `small` and `complete` profiles, use these sections in order. The `personal`
profile may use content-appropriate headings, including for portfolios and resume
generators; still explain applicable build and verification commands:

1. `## Quickstart` — prerequisites, installation and one runnable command with
   expected output. State any required service, credentials or hardware.
2. `## Usage` — a few common tasks; link to detailed instructions.
3. `## Verification` — commands that confirm the project works, and what they
   actually test. Distinguish discovery, offline checks and integration runs.
4. `## Documentation` — links and one-line purposes for maintained guides.
   Omit when the README is the only guide.
5. `## License` — applicable licensing information, last when present. Link an
   existing licence; do not invent an MIT licence for private or personal content.

Screenshots and a small overview diagram are optional when they explain the
result. Keep exhaustive configuration, troubleshooting and implementation detail
in guides. Aim for a README that can be read in five minutes.

## Maintained guides

| Guide | Contents |
| --- | --- |
| `docs/development.md` | Detailed setup, configuration, adding tests/features, checks, troubleshooting and exceptions |
| `docs/architecture.md` | Components, execution/data flow, external dependencies, boundaries and key decisions |

Optional guides should cover a distinct substantial topic, such as deployment
or a protocol. Keep each explanation in one authoritative place and link to it.
Preserve useful existing material when splitting or renaming guides; update
incoming links in the same change. Do not delete historical decisions for a quota.

## Formatting and diagrams

These rules are required; the Mermaid preference is a default.

- Use GitHub-Flavored Markdown, one H1 and sequential heading levels.
- Use lowercase kebab-case guide filenames; retain conventional root names such
  as `README.md`, `AGENTS.md` and `LICENSE`.
- Use relative links inside the repository and descriptive link labels.
- Label fenced code blocks with their language. Commands must state their working
  directory when it differs from the root; distinguish placeholders from literals.
- Use tables for comparisons and lists for steps. Avoid duplicate command catalogs.
- Prefer Mermaid for component, sequence or data-flow diagrams. Include a diagram
  when relationships are difficult to explain in prose; no decorative diagrams.
- Keep editable diagram source with exports in `docs/assets/`. Add descriptive
  alt text to images; generated images must not be the only diagram source.
- Update affected docs alongside behavior changes and check links after moves.

## Markdown linting

Adopting software repositories must lint maintained Markdown with
[markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2), using the same
configuration locally and in CI. See the [scope](../README.md#scope) for applicability.

Use the default rules with `MD013` (line length) disabled so tables, links and
commands do not need artificial wrapping. Keep heading, spacing, fenced-code
language and image-alt-text checks enabled. Record narrowly scoped exceptions
with a reason; avoid blanket rule disables to accommodate one file.

Store the baseline in the adopting repository's `.markdownlint-cli2.jsonc`:

```jsonc
{
  "config": {
    "default": true,
    "MD013": false
  }
}
```

Lint the root README, agent/community Markdown files and maintained guides.
Explicitly exclude dependencies, generated output and archived plans from the
selected paths. Historical exclusions must not hide current documentation.

In Node repositories, lock markdownlint-cli2 as a development dependency and
expose an `npm run lint:md` script. Python, Java and Swift repositories may use a pinned CLI or a
SHA-pinned lint action; document an equivalent local command without forcing
application code into a Node project. Never install an unbounded latest version
in CI. Run in check mode there; apply fixes locally and review the diff.

Linting checks Markdown conventions, not command correctness or link reachability.
Continue reviewing content and checking links when documents change.
