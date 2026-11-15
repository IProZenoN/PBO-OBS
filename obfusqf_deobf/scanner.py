"""Directory scanner for ObfuSQF-obfuscated missions.

Detects the three fingerprints described in the public ObfuSQF write-up:

1. split-string ``call compile(...)`` payloads,
2. ``*.rsa.sqf`` key files inside randomized folder trees,
3. references to the ``ObfuSQF`` loadFile guard.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .keys import RSA_SUFFIX, keys_from_text, keys_from_rsa_file
from .strings import count_split_sequences

OBFUSQF_DIR = re.compile(r"\bObfuSQF\b", re.IGNORECASE)
CALL_COMPILE = re.compile(r"call\s+compile\s*\(", re.IGNORECASE)

# Randomized path segments: lowercase alphanumeric, 8-12 chars, not a word.
_RANDOM_SEGMENT = re.compile(r"(?<![A-Za-z0-9])([a-z0-9]{8,12})(?![A-Za-z0-9])")


@dataclass
class ScanReport:
    root: Path
    files_scanned: int = 0
    obfuscated_files: list[str] = field(default_factory=list)
    rsa_key_files: list[str] = field(default_factory=list)
    keys: list[str] = field(default_factory=list)
    obfusqf_refs: list[str] = field(default_factory=list)
    randomized_paths: list[str] = field(default_factory=list)

    @property
    def is_obfuscated(self) -> bool:
        return bool(self.obfuscated_files or self.rsa_key_files or self.keys)


def _randomized_path_candidates(text: str) -> list[str]:
    """Path-like strings built mostly from random lowercase segments."""
    found: list[str] = []
    for candidate in re.findall(r'"([^"\n]*\\[^"\n]*)"', text):
        segments = re.split(r"\\+", candidate.strip("\\"))
        segments = [s for s in segments if s]
        if len(segments) < 2:
            continue
        randomish = [s for s in segments if _RANDOM_SEGMENT.fullmatch(s)]
        if len(randomish) >= max(2, len(segments) - 1):
            found.append(candidate)
    return found


def scan_file(path: Path) -> dict | None:
    """Analyze a single file; returns a small report dict or None."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    info: dict = {
        "path": str(path),
        "split_sequences": count_split_sequences(text),
        "call_compile": len(CALL_COMPILE.findall(text)),
        "obfusqf_refs": len(OBFUSQF_DIR.findall(text)),
        "randomized_paths": _randomized_path_candidates(text),
        "keys": [h.key for h in keys_from_text(text, source=str(path))],
    }

    if path.name.endswith(RSA_SUFFIX):
        hit = keys_from_rsa_file(path)
        if hit:
            info["keys"].append(hit.key)
            info["rsa_file"] = True

    return info


def scan_tree(root: Path) -> ScanReport:
    """Walk *root* and build a full ObfuSQF report."""
    report = ScanReport(root=root)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        report.files_scanned += 1
        info = scan_file(path)
        if info is None:
            continue

        if info.get("rsa_file"):
            report.rsa_key_files.append(info["path"])
        if info["split_sequences"] > 0 or info["call_compile"] > 0:
            report.obfuscated_files.append(info["path"])
        if info["obfusqf_refs"] > 0:
            report.obfusqf_refs.append(info["path"])
        report.randomized_paths.extend(info["randomized_paths"])
        for key in info["keys"]:
            if key not in report.keys:
                report.keys.append(key)
    return report
