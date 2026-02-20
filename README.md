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

Bruk

Plasser kof_to_dxf.py i samme mappe som .kof-filen.

Kjør:

python kof_to_dxf.py "innmaaling.kof" resultat.dxf
Valg
Parameter	Forklaring
--d=0.5	Diameter på markør (meter)
--text=ALL	Punktnavn + kote
--text=Z	Kun kote
--text=ID	Kun punktnavn
--text=NONE	Ingen tekst

Eksempel:

python kof_to_dxf.py "GV - Innmålt trau 25.01.2026.kof" trau.dxf --d=1.0 --text=Z
Åpne i AutoCAD

Åpne resultat.dxf

Zoom Extents (Z → E)

Lagre som DWG

Hvis grafikken oppfører seg rart (store koordinater):

REGENALL

eller slå av hardware acceleration (GRAPHICSCONFIG).

Dette er et kjent fenomen i CAD ved UTM-koordinater > 1 000 000.

Format som støttes

Scriptet forventer KOF-linjer omtrent slik:

05 P657 (0)             1216203.852  120379.229  117.036

Altså:

[punktkode] [punktnavn] (status) [Northing] [Easting] [Kote]
Begrensninger

Leser kun punktdata (ikke linjekoder/bruddlinjer)

Lager ikke automatisk terrengmodell (TIN)

Er ment som et kontroll- og visualiseringsverktøy, ikke en full landmålingsprogramvare

Hvorfor dette verktøyet finnes

Mange prosjekter får innmålinger levert i KOF uten DWG.
Å åpne disse krever normalt:

Novapoint

Gemini Terreng

Civil 3D

Dette verktøyet gir en rask, enkel og gratis vei fra feltdata til tegning.

Ansvar

Programmet brukes på eget ansvar.
Kontroller alltid kritiske mål før bygging eller stikning.
