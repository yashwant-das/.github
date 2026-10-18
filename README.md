# Repository standards

Shared standards and adoption tools for Yashwant Das's repositories. Documentation
comes first: readers should understand a project, get a first successful run, and
find deeper guidance without reading repeated instructions.

These standards also support explicit adoption by repositories owned by Shivani.
They do not rename, reorganize, or change existing projects automatically.

## Quickstart

Requires Python 3.13 and Node 24.

```sh
npm ci
npm test
npm run lint:docs
python3 scripts/validate_docs.py .
```

To check another repository after adding its `.standards.json`:

```sh
python3 scripts/validate_docs.py ../your-repository
```

## Usage

1. Choose a documentation profile from the documentation standard.
2. Use the README and guide templates, keeping only useful sections.
3. Add `.standards.json` and justify any additional maintained guides.
4. Run the validator locally. Fix findings before adding required checks.
5. After this repository is published, add the caller workflow using its full
   commit SHA in both the workflow reference and `standards-ref` input.
6. Pilot one complete framework and one starter before wider adoption.

Existing repository-specific agent instructions and compatibility constraints
still matter. Migrate incrementally; do not rewrite working layouts solely for
visual consistency.

## Verification

`npm test` runs regression tests for the validator. `npm run lint:docs` checks
Markdown formatting. The Python command checks the selected profile, required
files, README sections, maintained-guide discovery, and local Markdown file links.
It does not check external URL availability, heading anchors, Mermaid rendering,
or the quality of prose. See the development guide for precise limitations.

## Documentation

- [Documentation standard](docs/documentation.md): profiles, README contents,
  guide boundaries, formatting, diagrams, and additional-document policy.
- [Folder structure](docs/structure.md): shared conventions and stack layouts.
- [Dependencies](docs/dependencies.md): runtime baselines, stable library snapshots,
  compatibility, locking, and updates.
- [CI/CD](docs/cicd.md): required checks, reusable workflow, adoption, and deployments.
- [Development](docs/development.md): work on and test this repository.
- [Architecture](docs/architecture.md): how the checks and workflows fit together.
- [Roadmap](ROADMAP.md): rollout and later engineering standards.
- [README template](templates/README.template.md),
  [development template](templates/development.template.md),
  [architecture template](templates/architecture.template.md), and
  [adoption checklist](templates/adoption-checklist.md).

Historical implementation artifacts live under `docs/superpowers/`. They record
how this release was built; the maintained guides above define current standards.

## Contributions

See [CONTRIBUTING.md](CONTRIBUTING.md). This foundation is prepared locally;
publication, consumer onboarding, and required-check settings are separate steps.

## License

[MIT](LICENSE). This license covers this repository only; it does not supply a
license to other repositories through GitHub's default-file mechanism.
