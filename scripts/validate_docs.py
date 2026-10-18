#!/usr/bin/env python3
"""Validate the documented subset of repository documentation standards offline."""
import argparse
import fnmatch
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

PROFILES = {'small': (), 'personal': (),
            'complete': ('docs/development.md', 'docs/architecture.md'),
            'standards': ('docs/development.md', 'docs/architecture.md')}
IGNORED_PARTS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__',
                 'vendor', 'dist', 'build', 'playwright-report', 'test-results',
                 'allure-results', 'allure-report', '.superpowers'}
INLINE = re.compile(r'!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s()]+))(?:\s+["\'][^\n]*?["\'])?\s*\)')
REFERENCE = re.compile(r'^ {0,3}\[([^\]\n]+)\]:\s*(?:<([^>\n]+)>|(\S+))', re.MULTILINE)
REFERENCE_USE = re.compile(r'!?\[([^\]\n]+)\]\[([^\]\n]*)\]')


def prose(text):
    """Mask fenced and inline code while preserving line numbers."""
    lines = []
    fence_char, fence_size = '', 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence_char:
            if marker and marker[1][0] == fence_char and len(marker[1]) >= fence_size and not line[marker.end():].strip():
                fence_char = ''
            lines.append('\n')
        elif marker:
            fence_char, fence_size = marker[1][0], len(marker[1])
            lines.append('\n')
        else:
            lines.append(re.sub(r'(`+).*?\1', '', line))
    return ''.join(lines)


def links(text, include_definitions=True):
    """Yield conventional inline, full, collapsed, and shortcut reference links."""
    inline = list(INLINE.finditer(text))
    references = list(REFERENCE_USE.finditer(text))
    definitions = list(REFERENCE.finditer(text))
    targets = {m[1].strip().casefold(): (m[2] or m[3]) for m in definitions}
    for match in inline:
        yield match[1] or match[2], match.start()
    for match in references:
        label = (match[2] or match[1]).strip().casefold()
        if label in targets:
            yield targets[label], match.start()
    # Only standalone brackets count as shortcuts, never a definition or the
    # label/destination of an inline or explicit reference link.
    occupied = [(match.start(), match.end()) for match in (*inline, *references, *definitions)]
    for match in re.finditer(r'!?\[([^\]\n]+)\]', text):
        if any(start <= match.start() < end for start, end in occupied):
            continue
        opening = match.start() + int(match[0].startswith('!'))
        prefix = text[:opening]
        backslashes = len(prefix) - len(prefix.rstrip(chr(92)))
        if backslashes % 2:
            continue  # Escaped brackets render literal text rather than links.
        label = match[1].strip().casefold()
        if label in targets:
            yield targets[label], match.start()
    if include_definitions:
        for match in definitions:
            yield match[2] or match[3], match.start()


def local_target(root, source, destination):
    """Return (resolved path, escapes-root); external/anchor-only links return None."""
    parsed = urlsplit(destination)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None, False
    path = unquote(parsed.path)
    target = (root / path.lstrip('/') if path.startswith('/') else source.parent / path).resolve()
    return target, not target.is_relative_to(root)


def excluded(relative, patterns):
    candidates = [relative] + [parent.as_posix() + '/' for parent in Path(relative).parents if parent != Path('.')]
    return (bool(set(Path(relative).parts) & IGNORED_PARTS)
            or relative.startswith('docs/superpowers/')
            or any(fnmatch.fnmatchcase(candidate, pattern) for candidate in candidates for pattern in patterns))


def markdown_files(root, patterns):
    """Find Markdown once using the same exclusions for linting and validation."""
    import os
    paths = []
    for directory, subdirs, names in os.walk(root, followlinks=False):
        subdirs[:] = [name for name in subdirs if not excluded((Path(directory) / name).relative_to(root).as_posix() + '/', patterns)]
        for name in names:
            source = Path(directory) / name
            relative = source.relative_to(root).as_posix()
            if source.suffix.lower() == '.md' and not excluded(relative, patterns):
                paths.append(source)
    return sorted(paths)


def validate(root):
    """Return actionable findings for one repository; never fetch external content."""
    root = Path(root).resolve()
    findings = []
    try:
        config = json.loads((root / '.standards.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        return [f'.standards.json: invalid or missing configuration: {error}']
    if not isinstance(config, dict):
        return ['.standards.json: configuration must be an object']
    if set(config) - {'profile', 'exclude', 'additional_guides'}:
        return ['.standards.json: unknown configuration keys']
    profile = config.get('profile')
    if not isinstance(profile, str) or profile not in PROFILES:
        return ['.standards.json: profile must be small, complete, personal, or standards']
    patterns = config.get('exclude', [])
    extra = config.get('additional_guides', {})
    if not isinstance(patterns, list) or not all(isinstance(x, str) and x.strip() for x in patterns):
        return ['.standards.json: exclude must be a list of nonempty path patterns']
    if not isinstance(extra, dict) or not all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in extra.items()):
        return ['.standards.json: additional_guides must map paths to a nonempty rationale']
    for name in extra:
        path = Path(name)
        if not name.startswith('docs/') or path.suffix.lower() != '.md' or '..' in path.parts or excluded(name, patterns):
            findings.append(f'{name}: additional guide must be an active Markdown path under docs/')
    required = ('README.md',) + PROFILES[profile]
    for name in dict.fromkeys((*required, *extra)):
        if excluded(name, patterns):
            findings.append(f'{name}: required document cannot be excluded')
        path = root / name
        try:
            if not path.resolve().is_relative_to(root) or not path.read_text(encoding='utf-8').strip():
                findings.append(f'{name}: required document is empty or outside repository')
        except (OSError, UnicodeError):
            findings.append(f'{name}: required nonempty document is missing or unreadable')

    documents = {}
    for source in markdown_files(root, patterns):
        relative = source.relative_to(root).as_posix()
        if not source.resolve().is_relative_to(root):
            findings.append(f'{relative}: document is outside repository')
            continue
        try:
            documents[relative] = prose(source.read_text(encoding='utf-8'))
        except (OSError, UnicodeError):
            findings.append(f'{relative}: Markdown is unreadable or not UTF-8')
    guides = sorted(name for name in documents if name.startswith('docs/') and not name.startswith('docs/assets/'))
    for name in guides:
        if name not in PROFILES[profile] and name not in extra:
            findings.append(f'{name}: additional maintained guide needs a rationale in additional_guides')
    readme = documents.get('README.md', '')
    headings = list(re.finditer(r'^## ([^\n]+?)\s*$', readme, re.MULTILINE))
    expected = ['Quickstart', 'Usage', 'Verification'] if profile != 'personal' else []
    if guides:
        expected.append('Documentation')
    positions = []
    for name in expected:
        match = next((m for m in headings if m[1] == name), None)
        if match:
            positions.append(match.start())
        else:
            findings.append(f'README.md: missing ## {name}')
    if positions != sorted(positions):
        findings.append('README.md: required headings are out of order')
    doc_heading = next((m for m in headings if m[1] == 'Documentation'), None)
    if doc_heading:
        end = next((m.start() for m in headings if m.start() > doc_heading.start()), len(readme))
        section = readme[doc_heading.end():end]
        # Reference definitions may be located outside the Documentation section.
        section += '\n' + '\n'.join(m[0] for m in REFERENCE.finditer(readme))
        targets = set()
        for destination, _ in links(section, include_definitions=False):
            try:
                target, escape = local_target(root, root / 'README.md', destination)
            except ValueError:
                continue  # Link findings below provide the source diagnostic.
            if target and not escape:
                targets.add(target)
        for name in guides:
            if (root / name).resolve() not in targets:
                findings.append(f'README.md: Documentation must link to {name}')
    for name, text in documents.items():
        for destination, offset in links(text):
            try:
                target, escape = local_target(root, root / name, destination)
            except ValueError:
                findings.append(f'{name}: invalid link destination {destination}')
                continue
            line = text[:offset].count('\n') + 1
            if escape:
                findings.append(f'{name}:{line}: link outside repository: {destination}')
            elif target is not None and not target.exists():
                findings.append(f'{name}:{line}: missing local link target: {destination}')
    return list(dict.fromkeys(findings))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list-markdown', action='store_true', help='Output validated Markdown paths as JSON')
    parser.add_argument('repository', nargs='?', default='.')
    args = parser.parse_args()
    findings = validate(Path(args.repository))
    if findings:
        print('\n'.join(findings))
        return 1
    if args.list_markdown:
        root = Path(args.repository).resolve()
        config = json.loads((root / '.standards.json').read_text(encoding='utf-8'))
        print(json.dumps([p.relative_to(root).as_posix() for p in markdown_files(root, config.get('exclude', []))]))
    else:
        print('Documentation checks passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
