"""Real temporary repositories exercise the public validator and CLI contracts."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/validate_docs.py'


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write('README.md', '# Example\n\n## Quickstart\n\nRun it.\n\n## Usage\n\nUse it.\n\n## Verification\n\nCheck it.\n')
        self.config()

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def config(self, **kwargs):
        self.write('.standards.json', json.dumps({'profile': 'small', **kwargs}))

    def check(self):
        # The missing implementation must cause a real assertion failure at RED.
        self.assertTrue(SCRIPT.is_file(), 'documentation validator is not implemented')
        spec = importlib.util.spec_from_file_location('validate_docs', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.validate(self.root)

    def test_small_project_needs_no_empty_extra_guides(self):
        self.assertEqual(self.check(), [])

    def test_personal_readme_does_not_need_code_headings(self):
        self.config(profile='personal')
        self.write('README.md', '# Profile\n\nPersonal projects.\n')
        self.assertEqual(self.check(), [])

    def test_complete_project_requires_development_and_architecture(self):
        self.config(profile='complete')
        errors = '\n'.join(self.check())
        self.assertIn('docs/development.md', errors)
        self.assertIn('docs/architecture.md', errors)

    def test_complete_and_standards_profiles_accept_required_guides(self):
        for profile in ('complete', 'standards'):
            with self.subTest(profile=profile):
                self.config(profile=profile)
                self.write('docs/development.md', '# Development\n')
                self.write('docs/architecture.md', '# Architecture\n')
                self.write('README.md', '# Example\n\n## Quickstart\n\nRun.\n\n## Usage\n\nUse.\n\n## Verification\n\nTest.\n\n## Documentation\n\n[Develop](docs/development.md)\n[Design](docs/architecture.md)\n')
                self.assertEqual(self.check(), [])

    def test_exclusions_cannot_hide_profile_required_documents(self):
        self.write('docs/development.md', '# Development\n\n[Missing](missing.md)\n')
        self.write('docs/architecture.md', '# Architecture\n\n[Missing](missing.md)\n')
        for profile in ('complete', 'standards'):
            for pattern in ('docs/**', 'docs/', 'docs/development.md'):
                with self.subTest(profile=profile, pattern=pattern):
                    self.config(profile=profile, exclude=[pattern])
                    errors = '\n'.join(self.check())
                    self.assertIn('required document cannot be excluded', errors)
        self.config(profile='personal', exclude=['README.md'])
        self.assertIn('README.md: required document cannot be excluded', '\n'.join(self.check()))

    def test_missing_and_malformed_configuration_fail(self):
        (self.root / '.standards.json').unlink()
        self.assertIn('.standards.json', '\n'.join(self.check()))
        self.write('.standards.json', '{')
        self.assertIn('configuration', '\n'.join(self.check()))

    def test_invalid_schema_and_unknown_profiles_fail(self):
        for config in ([], {'profile':'typo'}, {'profile':'small', 'exclude':'docs'},
                       {'profile':'small','additional_guides':[]}, {'profile':'small','typo':True}):
            with self.subTest(config=config):
                self.write('.standards.json', json.dumps(config))
                self.assertTrue(self.check())

    def test_empty_required_document_fails(self):
        self.write('README.md', ' \n')
        self.assertIn('README.md', '\n'.join(self.check()))

    def test_missing_and_out_of_order_headings_fail(self):
        self.write('README.md', '# Example\n\n## Usage\n\n## Quickstart\n')
        errors = '\n'.join(self.check())
        self.assertIn('Verification', errors)
        self.assertIn('order', errors)

    def test_extra_guide_requires_rationale_and_readme_discovery(self):
        self.write('docs/cli.md', '# CLI\n')
        self.assertIn('rationale', '\n'.join(self.check()))
        self.config(additional_guides={'docs/cli.md':'Operators need CLI details'})
        self.assertIn('Documentation', '\n'.join(self.check()))
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n## Documentation\n\n[CLI](docs/cli.md)\n')
        self.assertEqual(self.check(), [])

    def test_unused_reference_definition_does_not_make_guide_discoverable(self):
        self.write('docs/cli.md', '# CLI\n')
        self.config(additional_guides={'docs/cli.md':'CLI reference'})
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n[CLI][cli]\n\n## Documentation\n\nNo guide link yet.\n\n[cli]: docs/cli.md\n')
        self.assertIn('must link', '\n'.join(self.check()))
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n[CLI][cli]\n')
        self.assertEqual(self.check(), [])

    def test_shortcut_and_explicit_references_make_guides_discoverable(self):
        self.write('docs/cli.md', '# CLI\n')
        self.config(additional_guides={'docs/cli.md':'CLI reference'})
        prefix = (self.root / 'README.md').read_text()
        for usage in ('[CLI]', '[cli]', '[CLI][]', '[Commands][CLI]'):
            with self.subTest(usage=usage):
                self.write('README.md', prefix + '\n## Documentation\n\n' + usage + '\n\n## Other\n\n[CLI]: docs/cli.md\n')
                self.assertEqual(self.check(), [])

    def test_inline_label_does_not_count_as_shortcut_reference(self):
        self.write('docs/cli.md', '# CLI\n')
        self.config(additional_guides={'docs/cli.md':'CLI reference'})
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n## Documentation\n\n[CLI](https://example.com)\n\n[CLI]: docs/cli.md\n')
        self.assertIn('must link', '\n'.join(self.check()))

    def test_declared_missing_guide_and_blank_rationale_fail(self):
        self.config(additional_guides={'docs/absent.md':'API reference'})
        self.assertIn('absent.md', '\n'.join(self.check()))
        self.config(additional_guides={'docs/api.md':' '})
        self.assertIn('rationale', '\n'.join(self.check()))

    def test_broken_links_and_images_report_source(self):
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n[Missing](absent.md)\n![Image](docs/assets/missing.png)\n')
        errors = '\n'.join(self.check())
        self.assertIn('README.md', errors)
        self.assertIn('absent.md', errors)
        self.assertIn('missing.png', errors)

    def test_reference_links_encoded_paths_and_directories(self):
        self.write('docs/assets/a b.txt','asset')
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n[Asset][asset]\n[Folder](docs/assets/)\n\n[asset]: docs/assets/a%20b.txt\n')
        self.assertEqual(self.check(), [])
        (self.root / 'docs/assets/a b.txt').unlink()
        self.assertIn('a%20b.txt', '\n'.join(self.check()))

    def test_fenced_examples_inline_code_and_external_links_are_ignored(self):
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n```md\n[Example](missing.md)\n```\n\n~~~md\n[Example](missing.md)\n~~~\n\n`[inline](absent.md)`\n[Site](https://example.com)\n[Mail](mailto:a@example.com)\n[Anchor](#unknown)\n')
        self.assertEqual(self.check(), [])

    def test_generated_vendor_and_historical_files_are_ignored(self):
        for path in ('node_modules/pkg/README.md','docs/superpowers/specs/history.md',
                     'playwright-report/index.md','custom-output/report.md'):
            self.write(path,'# Generated\n\n[Missing](absent.md)\n')
        self.config(exclude=['custom-output/**'])
        self.assertEqual(self.check(), [])

    def test_relative_escape_is_rejected(self):
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n[Outside](../outside.md)\n')
        self.assertIn('outside repository', '\n'.join(self.check()))

    def test_file_listing_shares_validator_exclusions(self):
        self.write('node_modules/a/README.md', '# Vendor\n')
        result = subprocess.run([sys.executable, str(SCRIPT), '--list-markdown', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), ['README.md'])

    def test_malformed_url_reports_finding_instead_of_crashing(self):
        self.config(profile='complete')
        self.write('docs/development.md', '# Development\n')
        self.write('docs/architecture.md', '# Architecture\n')
        with (self.root / 'README.md').open('a') as stream:
            stream.write('\n## Documentation\n\n[Invalid](https://[broken)\n')
        self.assertIn('invalid link', '\n'.join(self.check()))

    def test_cli_reports_success_and_nonzero_failure(self):
        self.assertTrue(SCRIPT.is_file(), 'documentation validator is not implemented')
        success = subprocess.run([sys.executable,str(SCRIPT),str(self.root)],capture_output=True,text=True)
        self.assertEqual(success.returncode,0,success.stderr)
        (self.root / 'README.md').unlink()
        failure = subprocess.run([sys.executable,str(SCRIPT),str(self.root)],capture_output=True,text=True)
        self.assertEqual(failure.returncode,1)
        self.assertIn('README.md',failure.stdout)


if __name__ == '__main__':
    unittest.main()
