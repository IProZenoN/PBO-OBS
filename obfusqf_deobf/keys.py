"""Extraction of ObfuSQF keys.

The whole "encryption" scheme stores its key inside the mission itself:

* a file named ``*.rsa.sqf`` whose raw content *is* the key, and/or
* a guard of the form ``loadFile "ObfuSQF\\...rsa.sqf") find "KEY" == -1``
  embedded in the compiled function — with ``==`` itself sometimes split
  into ``= '+'= ``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .strings import rejoin_strings

# loadFile "path.rsa.sqf") find "KEY"
LOADFILE_FIND = re.compile(
    r'loadFile\s+"([^"]*?\.rsa\.sqf)"\s*\)\s*find\s+"([^"]+)"',
    re.IGNORECASE,
)

# find "KEY" == -1  (key comparison guard; == may arrive split as "= =")
FIND_CMP = re.compile(r'find\s+"([^"]+)"\s*=\s*=?\s*=\s*-1')

RSA_SUFFIX = ".rsa.sqf"


@dataclass(frozen=True)
class KeyHit:
    key: str
    source: str
    kind: str


def keys_from_text(text: str, source: str = "<text>") -> list[KeyHit]:
    """Extract key candidates embedded in obfuscated SQF code."""
    merged = rejoin_strings(text)
    hits: dict[str, KeyHit] = {}
    for match in LOADFILE_FIND.finditer(merged):
        key = match.group(2)
        hits.setdefault(
            key, KeyHit(key=key, source=source, kind=f"loadFile {match.group(1)}")
        )
    for match in re.finditer(r'find\s+"([^"]+)"\s*=\s*=?\s*=\s*-1', merged):
        key = match.group(1)
        hits.setdefault(key, KeyHit(key=key, source=source, kind="find == -1 guard"))
    return list(hits.values())


def keys_from_rsa_file(path: Path) -> KeyHit | None:
    """Read a ``*.rsa.sqf`` key file; its whole trimmed content is the key."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    key = content.strip().strip('"').strip()
    if not key:
        return None
    return KeyHit(key=key, source=str(path), kind="rsa.sqf file")


def keys_from_tree(root: Path) -> list[KeyHit]:
    """Walk *root* and collect every key found (rsa.sqf files + code guards)."""
    hits: dict[str, KeyHit] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(RSA_SUFFIX):
            hit = keys_from_rsa_file(path)
            if hit:
                hits.setdefault(hit.key, hit)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for hit in keys_from_text(text, source=str(path)):
            hits.setdefault(hit.key, hit)
    return list(hits.values())
