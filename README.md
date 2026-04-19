# smi — Sheet Metal Optimisation Prototype

## Ziel

Prototyp zur LLM-basierten Bewertung des Optimierungspotenzials einer
Blechkonstruktion. Eingabe sind ein Bauteil-Bild (`.png`) und ein
Prüfplan (`.pdf`) pro übergeordnetem Optimierungspotenzial. Pro
Sub-Optimierungspotenzial wird ein unabhängiger, asynchroner Aufruf an
ein OpenAI Vision-LLM (via LangChain) ausgeführt, das Ergebnis wird per
Pydantic strukturiert zurückgegeben. Die Sub-Ratings werden zu einem
Gesamtrating aggregiert und in einen statischen HTML-Report geschrieben.

Kein RAG, keine PDF-Textextraktion — die vollständige PDF wird inline
(Base64) direkt in die Vision-Message übergeben.

## Projektstruktur

```
data/
  kb/sm/                       PNG-Bilder der Blechteile (z. B. SM01.png)
  optimisation_potential/      Prüfplan-PDFs je Potenzial (z. B. P01.pdf)
  schema/
    1_prompt.md                Basis-Prompt für das LLM
    optimisation_potential/    Markdown-Specs je Potenzial (P01.md, ...)
    sub_optimisation_potential/ Markdown-Specs je Subpotenzial (SP01_01.md, ...)
output/reports/                HTML-Reports (wird beim Lauf angelegt)
src/smi/
  main.py                      Entrypoint
  config/                      settings.py (.env), logging.py
  adapters/chat_model/         ChatOpenAI-Factory
  domain/schema/               Pydantic-Schemas (LLM vs. App)
  services/                    knowledge_base, assessment, report
  templates/report.html.j2     Jinja2-HTML-Template
```

## Konfiguration

Kopiere `.env.example` nach `.env` und trage mindestens den OpenAI-Key ein.

| Variable              | Default  | Zweck                                       |
| --------------------- | -------- | ------------------------------------------- |
| `OPENAI_API_KEY`      | —        | API-Key (erforderlich)                      |
| `OPENAI_MODEL`        | `gpt-4.1` | Vision- und PDF-fähiges Modell              |
| `LLM_MAX_CONCURRENCY` | `10`     | Max. parallele LLM-Calls in `abatch`        |
| `ROOT_LOG_LEVEL`      | `INFO`   | Root-Logger-Level                            |
| `SMI_LOG_LEVEL`       | `DEBUG`  | Level für den `smi`-Logger                   |

## Datenstruktur & Konvention

- **Bild**: `data/kb/sm/{sheet_metal_id}.png` — z. B. `SM01.png`.
- **Prüfplan**: `data/optimisation_potential/{potential_id}.pdf` — z. B.
  `P01.pdf`.
- **Subpotenziale** gehören über die Namenskonvention zum Parent:
  `SP{N}_*.md` → `P{N}`. Dadurch findet der Lauf automatisch alle zu
  einem Potenzial gehörenden Specs (z. B. `SP01_01.md`, `SP01_02.md`
  für `P01`).

## Ausführung

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -e .[dev]
cp .env.example .env   # OPENAI_API_KEY eintragen

python -m smi.main
```

Die Nutzer-Parameter `sheet_metal_id` und `optimisation_potential_ids`
werden oben in `src/smi/main.py` gesetzt:

```python
sheet_metal_id = "SM01"
optimisation_potential_ids = ["P01"]
```

## Bewertungslogik

Jeder LLM-Aufruf bewertet **ein** Sub-Optimierungspotenzial und gibt
strukturiert `rating`, `reason`, `evidence`, `confidence` zurück (Pydantic-
Schema `LLMSubPotentialAssessment`).

Das **Gesamtrating** eines übergeordneten Potenzials wird aggregiert:

- mindestens ein Subpotenzial `high` → Gesamt `high`
- sonst mindestens ein `medium` → Gesamt `medium`
- sonst (und mindestens ein erfolgreicher Sub-Call) → `low`
- wenn ausschließlich Fehler/keine Subs vorhanden → `none`

Fehlgeschlagene einzelne LLM-Calls (via `return_exceptions=True` bei
`abatch`) werden geloggt und mit Fehlermarker in den Report
aufgenommen — der Gesamtprozess bricht nicht ab.

## Report-Erzeugung

Pro Lauf wird ein statischer HTML-Report erzeugt:

```
output/reports/{sheet_metal_id}_{YYYYMMDD_HHMMSS}.html
```

Der Report enthält:

- Das Bild der Blechkonstruktion (eingebettet als Data-URL).
- Eine Übersichtstabelle aller geprüften Potenziale mit Gesamtrating.
- Pro Potenzial einen Block mit Name, ID, Gesamtrating-Badge und allen
  Subpotenzialen (Name, ID, Prüfungs-Typ, Rating-Badge, Begründung,
  Evidence-Liste, Confidence in %).
- Farbige Badges: `low` = grün, `medium` = orange, `high` = rot.

Das Template liegt in `src/smi/templates/report.html.j2` und ist
self-contained (kein externes CSS/JS).

## Diagramme rendern

Die Architektur- und Prozess-Diagramme liegen als Mermaid-Quellen unter
`docs/2_diagrams/src/` und werden als SVG nach
`docs/2_diagrams/rendered/` kompiliert. Voraussetzung: **Node.js / npx**.

```bash
for f in docs/2_diagrams/src/*.mmd; do
  name=$(basename "$f" .mmd)
  npx -y -p @mermaid-js/mermaid-cli mmdc -i "$f" -o "docs/2_diagrams/rendered/$name.svg"
done
```

```powershell
Get-ChildItem "docs/2_diagrams/src/*.mmd" | ForEach-Object {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    npx -y -p @mermaid-js/mermaid-cli mmdc -i $_.FullName -o "docs/2_diagrams/rendered/$name.svg"
}
```
