"""obfusqf_deobf — deobfuscator for ObfuSQF-protected Arma 3 missions."""

from .deobfuscate import DeobfuscationResult, deobfuscate
from .keys import KeyHit, keys_from_text, keys_from_tree
from .scanner import ScanReport, scan_file, scan_tree
from .strings import count_split_sequences, looks_obfuscated, rejoin_strings

__all__ = [
    "DeobfuscationResult",
    "KeyHit",
    "ScanReport",
    "count_split_sequences",
    "deobfuscate",
    "keys_from_text",
    "keys_from_tree",
    "looks_obfuscated",
    "rejoin_strings",
    "scan_file",
    "scan_tree",
]
__version__ = "0.1.0"
