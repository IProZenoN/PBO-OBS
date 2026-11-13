from obfusqf_deobf.deobfuscate import deobfuscate
from obfusqf_deobf.keys import keys_from_text, keys_from_tree
from obfusqf_deobf.scanner import scan_tree
from obfusqf_deobf.strings import (
    count_split_sequences,
    looks_obfuscated,
    rejoin_strings,
)

OBFUSCATED = (
    "[]call compile('i'+'f('+'isS'+'erver)exi'+'tWit'+'h();"
    "if((lo'+'adF'+'ile \"O'+'bf'+'uS'+'Q'+'F'+'pjjboo0shh\\arrdyhg2n3.rs'+'a.sq'+'f\") "
    "fi'+'nd \"ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir\") = '+'= -1)th'+'en("
    "pre'+'proc'+'essFi'+'le \"VGJHIMEI\\ITTSKCTE.sqf\");');"
)

PLAIN = 'if(!isServer) exitWith {};\nhint "hello world";'


class TestStrings:
    def test_rejoin_merges_chunks(self):
        assert rejoin_strings("'i'+'f('+'isS'+'erver") == "'if(isServer"

    def test_rejoin_supports_slash_variant(self):
        assert rejoin_strings("""'lo'/'adF'/'ile""") == "'loadFile"

    def test_rejoin_keeps_plain_code(self):
        assert rejoin_strings(PLAIN) == PLAIN

    def test_rejoin_keeps_non_adjacent_plus(self):
        text = "hint 'a' + x + 'b';"
        assert rejoin_strings(text) == text

    def test_count_and_flag(self):
        assert count_split_sequences(OBFUSCATED) > 0
        assert looks_obfuscated(OBFUSCATED)
        assert not looks_obfuscated(PLAIN)


class TestKeys:
    def test_keys_from_loadfile_guard(self):
        hits = keys_from_text(OBFUSCATED)
        assert "ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir" in [h.key for h in hits]

    def test_no_keys_in_plain_code(self):
        assert keys_from_text(PLAIN) == []


class TestDeobfuscate:
    def test_result_flags_and_code(self):
        result = deobfuscate(OBFUSCATED)
        assert result.was_obfuscated
        assert result.split_sequences > 0
        assert "'+'" not in result.code
        assert "loadFile" in result.code
        assert ".rsa.sqf" in result.code

    def test_plain_code_passthrough(self):
        result = deobfuscate(PLAIN)
        assert not result.was_obfuscated
        assert result.code == PLAIN


class TestScanner:
    def test_scan_tree_detects_sample(self, tmp_path):
        (tmp_path / "mission.sqf").write_text(OBFUSCATED, encoding="utf-8")
        rsa = tmp_path / "ObfuSQF" / "abc123xy" / "def456uv.rsa.sqf"
        rsa.parent.mkdir(parents=True)
        rsa.write_text("ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir\n", encoding="utf-8")

        report = scan_tree(tmp_path)
        assert report.is_obfuscated
        assert report.files_scanned == 2
        assert any(p.endswith("mission.sqf") for p in report.obfuscated_files)
        assert len(report.rsa_key_files) == 1
        assert "ZP7CEI1MML39P9feyJhMtpTPG0dff7V4n+esAA09hir" in report.keys

    def test_scan_clean_tree(self, tmp_path):
        (tmp_path / "init.sqf").write_text(PLAIN, encoding="utf-8")
        report = scan_tree(tmp_path)
        assert not report.is_obfuscated
