# Documentation standard

Rules for documentation in every repository that follows these standards.

## Profiles

| Profile | Required documents |
| --- | --- |
| `small` | README |
| `complete` | README, development guide, architecture guide |
| `personal` | README (code headings optional) |

Choose `personal` for portfolio content. Use `complete` when presenting a
project as a maintained application for other developers. Promote the profile
when complexity grows.

## README sections

Every non-personal README must include these headings in order:

1. `## Quickstart` — prerequisites, install steps, and one runnable command
   with expected output.
2. `## Usage` — common tasks after the first run.
3. `## Verification` — how to confirm the project works locally.
4. `## Documentation` — links to every maintained guide. Omit for `small`
   projects where the README is the only document.
5. `## License` — always the final section.

## Maintained guides

| Guide | Purpose |
| --- | --- |
| `docs/development.md` | Setup, configuration, checks, troubleshooting |
| `docs/architecture.md` | Components, data flow, decisions, boundaries |

`complete` profiles require both.

## Formatting

- Use GitHub-Flavored Markdown.
- Prefer Mermaid fenced blocks for diagrams so they render on GitHub and stay
  in version control.
- Do not commit generated images as the only representation of a diagram.
