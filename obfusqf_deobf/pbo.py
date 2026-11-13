"""PBO archive reader and ObfuSQF scanner.

PBO layout (BI addon format):

    [4 zero bytes]                          (addon signature, optional)
    filename\\0 magic u32 packing u32 original u32 timestamp u32 size u32
    ... more entries ...
    \\0                                      (empty name = end of header)
    <file data blobs, in entry order>

Only unpacked entries (packing = 0) are read; compressed PBO entries are
reported but skipped.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path

from .keys import KeyHit, keys_from_text
from .strings import count_split_sequences

ENTRY_HEADER = struct.Struct("<5I")
TEXT_SUFFIXES = {".sqf", ".sqm", ".cpp", ".hpp", ".h", ".hh", ".txt", ".inc", ".ext", ".csv"}


@dataclass(frozen=True)
class PboEntry:
    name: str
    magic: int
    packing: int
    original_size: int
    timestamp: int
    data_size: int
    data_offset: int


@dataclass
class PboReport:
    path: Path
    entries: list[PboEntry] = field(default_factory=list)
    keys: list[KeyHit] = field(default_factory=list)
    obfuscated_entries: list[str] = field(default_factory=list)
    skipped_compressed: list[str] = field(default_factory=list)

    @property
    def is_obfuscated(self) -> bool:
        return bool(self.keys or self.obfuscated_entries)


def read_pbo_entries(path: Path) -> list[PboEntry]:
    """Parse the PBO header and return entries with resolved data offsets."""
    raw: list[tuple[str, int, int, int, int, int]] = []
    with path.open("rb") as handle:
        first = handle.read(4)
        pos = 4 if first == b"\x00\x00\x00\x00" else 0
        handle.seek(pos)
        while True:
            name_bytes = bytearray()
            while True:
                char = handle.read(1)
                if not char:
                    return _with_offsets(path, raw, handle.tell())
                if char == b"\x00":
                    break
                name_bytes += char
            name = name_bytes.decode("ascii", errors="replace")
            if name == "":
                break
            header = handle.read(ENTRY_HEADER.size)
            if len(header) < ENTRY_HEADER.size:
                break
            magic, packing, original_size, timestamp, data_size = ENTRY_HEADER.unpack(header)
            raw.append((name, magic, packing, original_size, timestamp, data_size))
        return _with_offsets(path, raw, handle.tell())


def _with_offsets(
    path: Path,
    raw: list[tuple[str, int, int, int, int, int]],
    data_start: int,
) -> list[PboEntry]:
    entries: list[PboEntry] = []
    offset = data_start
    for name, magic, packing, original_size, timestamp, data_size in raw:
        entries.append(
            PboEntry(name, magic, packing, original_size, timestamp, data_size, offset)
        )
        offset += data_size
    return entries


def extract_entry(path: Path, entry: PboEntry) -> bytes:
    with path.open("rb") as handle:
        handle.seek(entry.data_offset)
        return handle.read(entry.data_size)


def _entry_text(path: Path, entry: PboEntry) -> str:
    return extract_entry(path, entry).decode("utf-8", errors="replace")


def scan_pbo(path: Path) -> PboReport:
    """Scan every readable entry of a .pbo for ObfuSQF keys and payloads."""
    report = PboReport(path=path)
    for entry in read_pbo_entries(path):
        report.entries.append(entry)
        lower = entry.name.lower()
        if entry.packing != 0:
            report.skipped_compressed.append(entry.name)
            continue
        if lower.endswith(".rsa.sqf"):
            key = _entry_text(path, entry).strip().strip('"').strip()
            if key:
                report.keys.append(
                    KeyHit(key=key, source=f"{path}:{entry.name}", kind="rsa.sqf in pbo")
                )
        suffix = Path(entry.name).suffix.lower()
        if entry.data_size and suffix in TEXT_SUFFIXES:
            text = _entry_text(path, entry)
            if count_split_sequences(text) or keys_from_text(text):
                report.obfuscated_entries.append(entry.name)
                report.keys.extend(keys_from_text(text, source=f"{path}:{entry.name}"))
    return report


def find_pbos(paths: list[Path]) -> list[Path]:
    """Expand directories into every contained .pbo; keep explicit files."""
    found: list[Path] = []
    for path in paths:
        if path.is_dir():
            found.extend(sorted(path.rglob("*.pbo")))
        elif path.suffix.lower() == ".pbo":
            found.append(path)
    return found


def extract_pbo(path: Path, dest: Path) -> list[Path]:
    """Write every entry of the archive under *dest*; returns written paths."""
    written: list[Path] = []
    for entry in read_pbo_entries(path):
        if entry.packing != 0 or not entry.data_size:
            continue
        target = dest.joinpath(*entry.name.split("\\"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(extract_entry(path, entry))
        written.append(target)
    return written
