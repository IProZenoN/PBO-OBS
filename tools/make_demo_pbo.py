# -*- coding: utf-8 -*-
"""Construit un PBO de démonstration imitant un addon ObfuSQF protégé."""
import struct
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "samples" / "demo_addon.pbo"

KEY = "XP7CZIIMRI39P9fsyJbhMpYFG0Odff7V4m+essA09hir"

CONFIG_CPP = """class CfgPatches {
    class ALF_Demo {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
    };
};
class CfgFunctions {
    class MAV_Sub {
        tag = "MAV";
        class client {
            file = "MAV_Sub";
            class init {};
        };
    };
};
"""

FUNCTIONS_HPP = """class MAV_Sub {
    class client {
        file = "MAV_Sub";
        class init {};
    };
};
"""

FN_INIT = (
    "[]call compile('i'+'f('+'isS'+'erver)exi'+'tWit'+'h();if((lo'+'adF'+'ile \"O'+'bf'+'uS'+'Q'+'F'+'\\'+'pjjboo0shh\\arrdyhg2n3\\wqdbfn113f\\lcmixn5bwv\\slgpvk8qzo\\ec1utgmpks\\swhieoq8fz\\pslnmmw1wr.rs"
    + "'+'a.sq'+'f\") fi'+'nd \"" + KEY + "\") = '+'= -1)th'+'en(pre'+'proc'+'essFi'+'le \"VGJHIMEI\\UNN15IME\\INTLC8NN\\ENNNIC18\\R0PK00N\\A11885SR\\IN115TC5\\ITTSKCTE.sqf\";"
    + "[] ex'+'ec'+'VM \"VGJHIMEI\\UNN15IME\\INTLC8NN\\ENNNIC18\\R0PK00N\\A11885SR\\IN115TC5\\ITTSKCTE.sqf\";"
    + "[]spa'+'wn(w'+'hile{tr'+'ue}d'+'o{\"Ev'+'ery'+'one'+'Los'+'t'+'\"'+' '+'c'+'a'+'ll BI'+'S'+'_f'+'nc'+'_en'+'d'+'Mis'+'sio'+'nServer;});};');\n"
)

DESCRIPTION_EXT = """respawn = "BASE";
respawnDelay = 30;
author = "demo";
"""

RSA_SQF = KEY + "\n"

LOGO_PAA = bytes.fromhex("0050414102000000") + bytes(range(64))  # en-tête PAA factice


def build_pbo(entries) -> bytes:
    out = b"\x00\x00\x00\x00"
    for name, data in entries:
        out += name.encode("ascii") + b"\x00"
        out += struct.pack("<5I", 0, 0, len(data), 0, len(data))
    out += b"\x00"
    for _, data in entries:
        out += data
    return out


entries = [
    ("config.cpp", CONFIG_CPP.encode("utf-8")),
    ("Functions.hpp", FUNCTIONS_HPP.encode("utf-8")),
    ("description.ext", DESCRIPTION_EXT.encode("utf-8")),
    ("MAV_Sub\\fn_init.sqf", FN_INIT.encode("utf-8")),
    ("ObfuSQF\\pjjboo0shh\\arrdyhg2n3\\wqdbfn113f\\lcmixn5bwv\\slgpvk8qzo\\ec1utgmpks\\swhieoq8fz\\pslnmmw1wr.rsa.sqf", RSA_SQF.encode("utf-8")),
    ("textures\\logo.paa", LOGO_PAA),
]

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(build_pbo(entries))
print("PBO de démo généré :", OUT, f"({OUT.stat().st_size} octets)")
