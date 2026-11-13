"""Command line interface for the ObfuSQF deobfuscator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .deobfuscate import deobfuscate
from .keys import keys_from_tree
from .scanner import scan_tree


def _cmd_deobfuscate(args: argparse.Namespace) -> int:
    if args.file == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        path = Path(args.file)
        if not path.is_file():
            print(f"error: file not found: {path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8", errors="replace")
        source = str(path)

    result = deobfuscate(text)
    if args.json:
        import json

        print(
            json.dumps(
                {
                    "source": source,
                    "was_obfuscated": result.was_obfuscated,
                    "split_sequences": result.split_sequences,
                    "keys": [k.key for k in result.keys],
                    "guard_paths": result.guard_paths,
                    "code": result.code,
                },
                indent=2,
            )
        )
        return 0

    print(f"source: {source}")
    print(f"obfuscated: {'yes' if result.was_obfuscated else 'no'}")
    if result.split_sequences:
        print(f"split-string sequences merged: {result.split_sequences}")
    for key in result.keys:
        print(f"key ({key.kind}): {key.key}")
    for guard in result.guard_paths:
        print(f"guard path: {guard}")
    print("--- deobfuscated code ---")
    print(result.code)
    return 0


def _cmd_keys(args: argparse.Namespace) -> int:
    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 1
    hits = keys_from_tree(root)
    if not hits:
        print("no keys found")
        return 0
    for hit in hits:
        print(f"{hit.key}\t[{hit.kind}]\t{hit.source}")
    return 0


def _cmd_scan(args: argparse.Namespace) -> int:
    root = Path(args.path)
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 1
    report = scan_tree(root)
    print(f"root: {report.root}")
    print(f"files scanned: {report.files_scanned}")
    print(f"obfuscated mission: {'YES' if report.is_obfuscated else 'no'}")
    if report.rsa_key_files:
        print("rsa.sqf key files:")
        for path in report.rsa_key_files:
            print(f"  {path}")
    if report.keys:
        print("keys:")
        for key in report.keys:
            print(f"  {key}")
    if report.obfuscated_files:
        print("files with obfuscated code:")
        for path in report.obfuscated_files:
            print(f"  {path}")
    if report.obfusqf_refs:
        print("files referencing ObfuSQF:")
        for path in report.obfusqf_refs:
            print(f"  {path}")
    if report.randomized_paths:
        print("randomized path trees:")
        for path in sorted(set(report.randomized_paths)):
            print(f"  {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="obfusqf-deobf",
        description="Deobfuscator for ObfuSQF-protected Arma 3 missions.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_deob = sub.add_parser("deobfuscate", help="deobfuscate an SQF file or stdin")
    p_deob.add_argument("file", help="path to the .sqf file, or '-' for stdin")
    p_deob.add_argument("--json", action="store_true", help="machine-readable output")
    p_deob.set_defaults(func=_cmd_deobfuscate)

    p_keys = sub.add_parser("keys", help="extract every key found under a path")
    p_keys.add_argument("path", help="mission or mod directory")
    p_keys.set_defaults(func=_cmd_keys)

    p_scan = sub.add_parser("scan", help="scan a mission/mod tree for ObfuSQF traces")
    p_scan.add_argument("path", help="mission or mod directory")
    p_scan.set_defaults(func=_cmd_scan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
