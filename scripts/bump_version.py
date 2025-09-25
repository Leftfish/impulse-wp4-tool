import argparse
import re
from pathlib import Path


CONSTANTS_PATH = Path(__file__).resolve().parents[1] / 'constants.py'


def read_version_text() -> str:
    text = CONSTANTS_PATH.read_text(encoding='utf-8')
    m = re.search(r'^APP_VERSION\s*=\s*"(\d+)\.(\d+)\.(\d+)\.(\d+)"', text, flags=re.M)
    if not m:
        raise RuntimeError('APP_VERSION not found in constants.py')
    return text


def parse_version(text: str):
    m = re.search(r'^APP_VERSION\s*=\s*"(\d+)\.(\d+)\.(\d+)\.(\d+)"', text, flags=re.M)
    return tuple(int(g) for g in m.groups())


def format_version(a: int, b: int, c: int, d: int) -> str:
    return f'{a}.{b}.{c}.{d}'


def bump(a: int, b: int, c: int, d: int, part: str):
    if part == 'A':
        return a + 1, 0, 0, 0
    if part == 'B':
        return a, b + 1, 0, 0
    if part == 'C':
        return a, b, c + 1, 0
    if part == 'D':
        return a, b, c, d + 1
    raise ValueError('part must be one of A, B, C, D')


def write_version(text: str, new_version: str):
    new_text = re.sub(
        r'^(APP_VERSION\s*=\s*")\d+\.\d+\.\d+\.\d+("\s*)$',
        rf'\g<1>{new_version}\2',
        text,
        flags=re.M,
    )
    CONSTANTS_PATH.write_text(new_text, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Bump A.B.C.D version in constants.py')
    parser.add_argument('--part', choices=['A', 'B', 'C', 'D'], required=True)
    args = parser.parse_args()

    text = read_version_text()
    a, b, c, d = parse_version(text)
    a, b, c, d = bump(a, b, c, d, args.part)
    new_version = format_version(a, b, c, d)
    write_version(text, new_version)
    print(new_version)


if __name__ == '__main__':
    main()


