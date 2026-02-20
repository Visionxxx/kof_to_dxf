#!/usr/bin/env python3
# kof_to_dxf.py
#
# Leser KOF på format omtrent:
#   05 P657 (0)             1216203.852  120379.229  117.036
#                 ^ N (Northing)          ^ E (Easting)  ^ Z
#
# Skriver DXF med ekte koordinater (E,N,Z) og MARKØRER I 3D (ikke z=0).
# Markør: sirkel + kryss med diameter d (default 0.5 m = 500 mm)

import re
import sys
from pathlib import Path
import ezdxf

LINE_RE = re.compile(
    r"^\s*(\d+)\s+([A-Za-z0-9_.-]+)\s+\(\s*\d+\s*\)\s+"
    r"([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)\s*$"
)

def parse_kof(path: Path):
    pts = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = LINE_RE.match(ln)
        if not m:
            continue
        code = m.group(1)
        pid  = m.group(2)
        n    = float(m.group(3))
        e    = float(m.group(4))
        z    = float(m.group(5))
        # AutoCAD WCS: X=E, Y=N
        pts.append((code, pid, e, n, z))
    return pts

def add_marker_3d(msp, x, y, z, d=0.5, layer="PUNKTER"):
    r = d / 2.0
    msp.add_circle((x, y, z), r, dxfattribs={"layer": layer})
    msp.add_line((x - r, y, z), (x + r, y, z), dxfattribs={"layer": layer})
    msp.add_line((x, y - r, z), (x, y + r, z), dxfattribs={"layer": layer})

def main():
    if len(sys.argv) < 3:
        print("Bruk: python kof_to_dxf.py input.kof output.dxf [--d=0.5] [--text=Z|ID|ALL|NONE]")
        sys.exit(2)

    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])

    d = 0.5
    text_mode = "ALL"
    for a in sys.argv[3:]:
        if a.startswith("--d="):
            d = float(a.split("=", 1)[1])
        elif a.startswith("--text="):
            text_mode = a.split("=", 1)[1].strip().upper()

    pts = parse_kof(inp)
    if not pts:
        raise SystemExit("Fant ingen punkter. (Parseren traff ikke KOF-formatet.)")

    # Ren DXF (ikke setup=True) for å unngå den offset-advarselen du fikk
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = ezdxf.units.M
    doc.header["$INSUNITS"] = 6        # meters
    doc.header["$MEASUREMENT"] = 1     # metric

    msp = doc.modelspace()

    # Layers
    for lname in ("PUNKTER", "TEKST_ID", "TEKST_Z"):
        if lname not in doc.layers:
            doc.layers.new(lname)

    # Tekststørrelse i meter
    text_h = max(0.20, d * 0.4)   # min 200 mm
    off    = d * 0.8

    # Sanity info (nyttig å se at Z ikke er 0)
    zs = [p[4] for p in pts]
    print(f"Punkter: {len(pts)} | Z min/max: {min(zs):.3f} / {max(zs):.3f}")

    for code, pid, x, y, z in pts:
        # Ekte 3D-point
        msp.add_point((x, y, z), dxfattribs={"layer": "PUNKTER"})

        # Synlig markør i 3D (på riktig kote)
        add_marker_3d(msp, x, y, z, d=d, layer="PUNKTER")

        # Tekst (legges også på riktig kote)
        if text_mode != "NONE":
            if text_mode in ("ALL", "ID"):
                msp.add_text(
                    pid,
                    dxfattribs={"layer": "TEKST_ID", "height": text_h}
                ).set_placement((x + off, y + off, z))

            if text_mode in ("ALL", "Z"):
                msp.add_text(
                    f"{z:.3f}",
                    dxfattribs={"layer": "TEKST_Z", "height": text_h}
                ).set_placement((x + off, y - off, z))

    doc.saveas(out)
    print(f"Skrev {out} (ekte E/N/Z på både punkt, markør og tekst).")

if __name__ == "__main__":
    main()