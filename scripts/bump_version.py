import argparse
import re
from pathlib import Path

CONSTANTS_PATH = Path(__file__).resolve().parents[1] / 'constants.py'

SEMVER_REGEX = r'^APP_VERSION\s*=\s*"(\d+)\.(\d+)\.(\d+)(?:-([\w.-]+))?(?:\+([\w.-]+))?"'

def read_version_text() -> str:
    text = CONSTANTS_PATH.read_text(encoding='utf-8')
    m = re.search(SEMVER_REGEX, text, flags=re.M)
    if not m:
        raise RuntimeError('APP_VERSION not found in constants.py')
    return text

def parse_version(text: str):
    m = re.search(SEMVER_REGEX, text, flags=re.M)
    if not m:
        raise RuntimeError('Invalid version format in constants.py')
    major, minor, patch, prerelease, build = m.groups()
    return int(major), int(minor), int(patch), prerelease or '', build or ''

def format_version(a: int, b: int, c: int, prerelease: str, build: str) -> str:
    version = f'{a}.{b}.{c}'
    if prerelease:
        version += f'-{prerelease}'
    if build:
        version += f'+{build}'
    return version

def bump(a: int, b: int, c: int, part: str, prerelease: str = '', build: str = ''):
    if part == 'A':
        return a + 1, 0, 0, '', ''
    if part == 'B':
        return a, b + 1, 0, prerelease, ''
    if part == 'C':
        return a, b, c + 1, prerelease, ''
    if part == 'PRERELEASE':
        if not prerelease:
            raise ValueError('Cannot bump prerelease without a valid identifier')
        return a, b, c, prerelease, ''
    if part == 'BUILD':
        if not build:
            raise ValueError('Cannot bump build without a valid identifier')
        return a, b, c, prerelease, build
    raise ValueError('part must be one of A, B, C, PRERELEASE, BUILD')

def write_version(text: str, new_version: str):
    new_text = re.sub(
        SEMVER_REGEX,
        rf'APP_VERSION = "{new_version}"',
        text,
        flags=re.M,
    )
    CONSTANTS_PATH.write_text(new_text, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description='Bump A.B.C, prerelease, or build metadata in constants.py')
    parser.add_argument('--part', choices=['A', 'B', 'C', 'PRERELEASE', 'BUILD'], required=True)
    parser.add_argument('--prerelease', help='Optional prerelease identifier (e.g., alpha, beta)')
    parser.add_argument('--build', help='Optional build metadata (e.g., build.1)')
    args = parser.parse_args()

    text = read_version_text()
    a, b, c, prerelease, build = parse_version(text)
    a, b, c, prerelease, build = bump(a, b, c, args.part, args.prerelease or prerelease, args.build or build)
    new_version = format_version(a, b, c, prerelease, build)
    write_version(text, new_version)
    print(new_version)

if __name__ == '__main__':
    main()