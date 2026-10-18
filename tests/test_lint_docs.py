"""Exercise the actual central Markdown lint runner against consumer content."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/lint_docs.mjs'


class MarkdownLintTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.standards.json').write_text(json.dumps({'profile':'personal'}))
        (self.root / 'README.md').write_text('# Example\n\nUseful project.\n')

    def run_lint(self):
        self.assertTrue(SCRIPT.is_file(), 'central Markdown lint runner is not implemented')
        return subprocess.run(['node',str(SCRIPT),str(self.root)],capture_output=True,text=True)

    def test_valid_consumer_passes_without_loading_consumer_js_configuration(self):
        (self.root / '.markdownlint.cjs').write_text("require('node:fs').writeFileSync('executed.txt','bad'); module.exports = {};")
        result = self.run_lint()
        self.assertEqual(result.returncode,0,result.stdout + result.stderr)
        self.assertFalse((self.root / 'executed.txt').exists())

    def test_bad_markdown_returns_nonzero_with_rule_and_filename(self):
        (self.root / 'README.md').write_text('# Example\n\n#### Skipped level\n')
        result = self.run_lint()
        self.assertEqual(result.returncode,1)
        self.assertIn('MD001',result.stdout)
        self.assertIn('README.md',result.stdout)

    def test_math_syntax_remains_compatible_with_patched_dependency(self):
        (self.root / 'README.md').write_text('# Formula\n\nInline $x^2$ and display:\n\n$$\nx^2 + y^2 = z^2\n$$\n')
        result = self.run_lint()
        self.assertEqual(result.returncode,0,result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
