# Folder structure standard

Required conventions follow; layouts marked “should” are defaults.

## Shared conventions

Create directories only when they hold something useful. A standard layout is a
navigation aid, not a requirement to populate empty folders.

| Path | Purpose |
| --- | --- |
| `README.md` | Project entry point and first successful run |
| `docs/` | Maintained guides |
| `docs/assets/` | Images and exported documentation diagrams |
| `scripts/` | Development and maintenance helpers |
| `.github/workflows/` | GitHub Actions workflows |
| `tests/` | Tests where the language or tool convention uses this path |

Keep manifests and tool configuration where the tools expect them. Keep secrets,
virtual environments, node_modules, browser state, reports, logs, and build output
out of Git. A deliberately committed example fixture is different from a run
artifact. Document safe sample configuration and provide `.env.example` if useful.

Preserve functional folders such as `tasks/`, `specs/`, agent definitions, Grafana
provisioning, or Appium capabilities. Explain them in the README or architecture
guide rather than renaming them to make different projects look identical.

## Python

Packaged Python projects should use:

```text
pyproject.toml
uv.lock
src/
  package_name/
tests/
docs/
```

Use `pyproject.toml` for project metadata and tooling, and uv for dependency
management. Existing pinned requirements workflows may remain as documented
exceptions under the dependency standard.
A short script demonstration can retain a flat structure. Pytest fixtures and
helpers belong near the tests that use them; avoid a catch-all utilities directory.

## Java

Maven projects should follow Maven's source layout:

```text
pom.xml
mvnw
.mvn/
src/
  main/java/
  main/resources/
  test/java/
  test/resources/
docs/
```

Test-only frameworks may omit `src/main/`. Keep source paths aligned with package
declarations and separate bundled sample application code from its test clients.
Prefer a Maven wrapper for repeatable builds; pin dependency and build-plugin
versions in the POM.

Java QA frameworks use `com.qaframework` as the Maven `groupId` and
`com.qaframework.<project>` as the base package. Use short, descriptive lowercase
project names such as `playwright`, `selenium` or `payments`, with functional
subpackages such as `config`, `pages`, `listeners` and `tests`. Avoid personal
names, redundant language segments and unclear abbreviations. Keep artifact IDs
descriptive, such as `qa-java-playwright`.

Other owners’ and client repositories retain their approved namespaces unless
they opt into this convention.

## JavaScript and TypeScript

Application/library projects normally use `src/` and `tests/`. Test-only Playwright
or WebdriverIO projects may have `tests/`, `pages/`, and `fixtures/` without `src/`.
Follow the established runner convention rather than forcing application folders.

```text
package.json
package-lock.json
playwright.config.ts
tests/
pages/
fixtures/
docs/
```

The example is for a test project; do not add Playwright files to unrelated apps.
Mixed Python/Node repositories keep each manifest at its real package root and
explain which runtime serves which component. Do not introduce a monorepo tool
merely to align layouts.

## Other projects and migration

Swift apps, portfolios, resumes, and reference notes retain their platform or
content conventions. Use the applicable documentation profile and explain unusual
paths. Existing projects migrate incrementally when changing related areas. Moving
files requires updating imports, tooling, CI, and documentation links together.
For Java package changes, also update suite/listener names, package scans, logging
and Maven module references. Review documentation and links as part of migration;
no shared validator is required.
