"""Print a Mardown matrix of wheels."""
from copy import deepcopy
from functools import cache
import sys
import httpx
import defopt
import json
import re
from packaging.utils import parse_wheel_filename
from wcwidth import wcswidth

__version__ = '0.1.0'


# Disregard any Python interpreter versions older than this
EOL_VERSION = (3, 7)


OS = str
Architecture = str
PyVersion = str


PLATFORMS = {
    'linux': ['x86_64', 'i686'],
    'windows': ['win32', 'amd64'],
    'mac': ['x86_64', 'arm64'],
}


Matrix = dict[tuple[PyVersion, OS, Architecture], bool]


def get_arch(tag: str) -> Architecture:
    if tag.endswith('_x86_64'):
        return 'x86_64'
    elif tag.endswith('_i686'):
        return 'i686'
    elif tag.endswith('_aarch64'):
        return 'aarch64'
    elif tag.endswith('_arm64'):
        return 'arm64'
    raise ValueError(f'Unknown architecture for {tag}')


def get_os_arch(tag: str) -> tuple[OS, Architecture]:
    if tag.startswith('manylinux'):
        return 'linux', get_arch(tag)
    if tag.startswith('musllinux'):
        return 'musllinux', get_arch(tag)
    elif tag == 'win32':
        return 'windows', 'win32'
    elif tag == 'win_amd64':
        return 'windows', 'amd64'
    elif tag.startswith('macosx'):
        return 'mac', get_arch(tag)
    raise ValueError(f'Unknown wheel target {tag}')


@cache
def get_cpython_versions() -> list[str]:
    """Get all released versions of CPython."""
    resp = httpx.get('https://www.python.org/ftp/python/').raise_for_status()
    found: set[tuple[int, ...]] = set()
    for v in re.findall(r'<a href="(\d+(?:\.\d+)+)/">', resp.text):
        k = tuple(int(component) for component in v.split('.'))
        found.add(k[:2])
    return [
        'cp{}{}'.format(*v)
        for v in sorted(found, reverse=True)
        if v > EOL_VERSION
    ]


def get_pypi_json(package: str) -> dict:
    """Get the JSON metadata about the given package."""
    return httpx.get(f'https://pypi.org/pypi/{package}/json').raise_for_status().json()


def identify_wheels(package: str, version: str | None = None, /):
    """Identify wheels for the given package and version.

    If version is not given it is the latest version of the package.
    """
    data = get_pypi_json(package)
    if version is None:
        version = data['info']['version']

    try:
        releases = data['releases'][version]
    except KeyError:
        sys.exit(f"{version} is not a valid version of {package}")

    pythons = get_cpython_versions()
    sdist = False
    matrix: Matrix = {}
    platforms = deepcopy(PLATFORMS)
    for r in releases:
        filename = r['filename']
        if filename.endswith('.whl'):
            pkg, v, build, tags = parse_wheel_filename(filename)
            for tag in tags:
                os, arch = get_os_arch(tag.platform)
                if arch not in platforms.setdefault(os, []):
                    platforms[os].append(arch)
                if tag.interpreter not in pythons:
                    pythons.append(tag.interpreter)
                matrix[tag.interpreter, os, arch] = True
        elif filename.endswith('.tar.gz'):
            sdist = True

    headers = ['Python']
    table = [headers]
    for os, archs in platforms.items():
        for arch in archs:
            headers.append(f'{os} {arch}')
    for python in pythons:
        row = [python]
        for os, archs in platforms.items():
            for arch in archs:
                has_wheel = matrix.get((python, os, arch), False)
                row.append('✅' if has_wheel else '❌')
        table.append(row)


    col_widths = [0] * len(table[0])
    for row in table:
        for i, v in enumerate(row):
            col_widths[i] = max(col_widths[i], wcswidth(v))
    table.insert(1, ['-' * w for w in col_widths])

    for row in table:
        print('| {} |'.format(
            ' | '.join(v + ' ' * (w - wcswidth(v)) for v, w in zip(row, col_widths))))


def main():
    defopt.run(identify_wheels)