"""High-level deobfuscation pipeline for ObfuSQF payloads."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .keys import LOADFILE_FIND, RSA_SUFFIX, KeyHit, keys_from_text
from .strings import count_split_sequences, rejoin_strings


@dataclass
class DeobfuscationResult:
    original: str
    code: str
    keys: list[KeyHit] = field(default_factory=list)
    guard_paths: list[str] = field(default_factory=list)
    split_sequences: int = 0

    @property
    def was_obfuscated(self) -> bool:
        return self.split_sequences > 0 or bool(self.guard_paths)


def deobfuscate(text: str) -> DeobfuscationResult:
    """Reassemble split strings and surface the embedded key material."""
    keys = keys_from_text(text)
    guard_paths = [m.group(1) for m in LOADFILE_FIND.finditer(rejoin_strings(text))]
    code = rejoin_strings(text)

    # Normalize the split "==" guard back into readable pseudo-SQF.
    code = re.sub(r"=\s*=\s*-1", "== -1", code)
    code = re.sub(r'= "+"= -1', "== -1", code)
    return DeobfuscationResult(
        original=text,
        code=code,
        keys=keys,
        guard_paths=guard_paths,
        split_sequences=count_split_sequences(text),
    )


def is_rsa_key_filename(name: str) -> bool:
    return name.endswith(RSA_SUFFIX)
