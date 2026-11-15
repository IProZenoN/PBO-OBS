"""Reassembly of ObfuSQF split string literals.

ObfuSQF chops SQF string literals into short single-quoted chunks and glues
them back together with ``+`` (or ``/`` in some variants) so the code looks
"more secure" at a glance — chunk boundaries can even fall inside what will
become a double-quoted path after reassembly:

    'i'+'f('+'isS'+'erver)exi'+'tWit'+'h();'
    loadFile "O'+'bf'+'uS'+'Q'+'F'+'pjjboo0shh\\....rs'+'a.sq'+'f")

Merging therefore means removing the quote/separator/quote joiners, which
collapses each run into a single single-quoted literal (SQF accepts both
quote styles).
"""

from __future__ import annotations

import re

# quote, separator (+ or /), quote — the ObfuSQF joiner.
_JOINER = re.compile(r"'\s*[+/]\s*'")


def rejoin_strings(text: str) -> str:
    """Collapse ObfuSQF joiners so split literals become single literals."""
    return _JOINER.sub("", text)


def count_split_sequences(text: str) -> int:
    """Number of ObfuSQF joiners found in *text* (obfuscation signal)."""
    return len(_JOINER.findall(text))


def looks_obfuscated(text: str) -> bool:
    """True when the text contains the ObfuSQF split-string signature."""
    return count_split_sequences(text) > 0
