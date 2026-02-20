# KOF → DXF (DWG) konverterer

Et lite Python-verktøy som konverterer norske landmålingsfiler i **KOF-format** (typisk Gemini/Novapoint/ISY) til **DXF**, slik at de kan åpnes direkte i AutoCAD, Civil 3D eller DWG TrueView — med ekte koordinater og riktig kote (Z).

Scriptet er laget for praktisk bruk i bygge- og anleggsprosjekter hvor man ofte får innmålinger levert som KOF, men trenger DWG for prosjektering, kontroll eller dokumentasjon.

---

## Hva scriptet gjør

- Leser inn KOF-punkter (E, N, Z)
- Beholder **ekte koordinater (UTM/EUREF)** — ingenting flyttes til lokalnull
- Oppretter:
  - 3D-punkt
  - synlig markør (sirkel + kryss)
  - punktnavn
  - kotehøyde
- Markørene ligger på korrekt Z (ikke z=0 slik mange konverteringer ender opp med)
- Skriver en stabil DXF (R2010) som kan lagres videre til DWG

Standard markørstørrelse: **0,5 m (500 mm)**

---

## Typisk bruk

Eksempler:
- Kontroll av entreprenørens stikning
- Sammenligning mot prosjektert modell
- Visualisering av terrengprofil
- Dokumentasjon av fundament, spor, VA eller bygg

---

## Krav

- Python 3.10+ (Windows fungerer helt fint)
- Ingen AutoCAD nødvendig for konvertering (kun for åpning)

Installer avhengighet:

```bash
pip install ezdxf
