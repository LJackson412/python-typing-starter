
## Getting Started

Python 3.12 empfohlen.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

## Diagramme rendern

Die Architektur- und Prozess-Diagramme liegen als Mermaid-Quellen unter `docs/2_diagrams/src/` und werden als SVG nach `docs/2_diagrams/rendered/` kompiliert. Voraussetzung: **Node.js / npx** verfügbar.

Einzelnes Diagramm rendern:

```bash
npx -y -p @mermaid-js/mermaid-cli mmdc \
  -i docs/2_diagrams/src/1_audit_process.mmd \
  -o docs/2_diagrams/rendered/1_audit_process.svg
```

Alle Diagramme in einem Rutsch (bash/powershell):

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

Du arbeitest in einem bestehenden Python-Projekt.

Ziel:
Implementiere einen einfachen Prototyp, der das Optimierungspotenzial einer Blechkonstruktion anhand eines Bildes, eines Prüfplans, eines Prompts und strukturierter Pydantic-Schemas mit einem OpenAI Vision-LLM bewertet und anschließend einen HTML-Report erzeugt.

Wichtig:
- Halte die Lösung einfach, verständlich und prototypisch.
- Nutze Best Practices, aber vermeide Overengineering.
- Bestehende Struktur darf sinnvoll angepasst werden.
- Benenne Module/Dateien bei Bedarf um, aber achte auf einheitliches Naming.
- Keine Tests implementieren.
- Kein RAG.
- Keine PDF-Textextraktion: Die vollständige PDF soll direkt an das LLM übergeben werden.
- Arbeite zuerst die bestehende Projektstruktur kurz durch und implementiere dann minimal-invasiv.

Technische Vorgaben:
- Framework: LangChain
- Verwende `ChatOpenAI` aus `langchain_openai`.
- Nutze die bestehende Factory:
  `smi/src/smi/adapters/chat_model/factory.py`
- Die Factory soll verwendet werden. Nur ändern, wenn wirklich nötig.
- Das Modell muss Vision unterstützen.
- Konfiguration über `.env`:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL`
  - `LLM_MAX_CONCURRENCY`
- Wähle sinnvolle Defaults, falls Werte fehlen.
- Verwende asynchrone Batch-Ausführung mit `abatch`.
- Limitiere die Concurrency über `RunnableConfig` auf `LLM_MAX_CONCURRENCY`, Default: `10`.

Eingabeparameter:
Die Anwendung soll als einfaches Python-Script ausführbar sein.

Der Nutzer muss vor dem Lauf definieren können:

```python
sheet_metal_id = "SM01"
optimisation_potential_ids = ["P01"]
````

Die Bilddatei wird über `sheet_metal_id` bestimmt:

```text
DEFAULT_SHEET_METAL_IMAGE_DIR = "smi/data/kb/sm"
Bildpfad: smi/data/kb/sm/{sheet_metal_id}.png
Beispiel: smi/data/kb/sm/SM01.png
```

Datenstruktur:

* Bilder der Blechkonstruktionen:
  `smi/data/kb/sm`
* Prüfpläne:
  `smi/data/optimisation_potential`
  Beispiel:
  `smi/data/optimisation_potential/P01.pdf`
* Fachliche Markdown-Beschreibungen für Schemas:
  `smi/data/schema`
* Übergeordnete Optimierungspotenziale:
  `smi/data/schema/optimisation_potential`
* Sub-Optimierungspotenziale:
  `smi/data/schema/sub_optimisation_potential`
* Prompt für Prüfung:
  `smi/data/schema/1_prompt.md`

Fachliche Logik:

* Jedes übergeordnete Optimierungspotenzial, z. B. `P01`, hat einen eigenen Prüfplan.
* Der Prüfplan gilt für alle zugehörigen Sub-Optimierungspotenziale.
* Beispiel:
  `smi/data/optimisation_potential/P01.pdf` wird für die Subpotenziale von `P01` verwendet.
* Aktuell existiert nur `P01`, später kommen weitere übergeordnete Potenziale hinzu.
* Aktuell existiert nur ein Bild, später kommen weitere Bilder hinzu.

Schemas:
Lege die Pydantic-Schemas hier an:

```text
smi/src/smi/domain/schema
```

Wichtig:
Es muss klar zwischen LLM-Schemas und Application-Schemas unterschieden werden.

LLM-Schemas:

* Enthalten nur Felder, die das LLM wirklich ausfüllen soll.
* Werden mit `with_structured_output(...)` verwendet.
* Verwende `ConfigDict(extra="forbid")`.
* Nutze aussagekräftige `Field(description=...)`.

Application-Schemas:

* Erweitern die LLM-Schemas um interne Felder, z. B. Metadaten, Pfade, IDs oder Daten für den Report.
* Enthalten Factory-Methoden wie `from_llm(...)`, wenn sinnvoll.

Orientiere dich am folgenden Muster:

```python
class LLM...Assessment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ...

class ...Assessment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ...

    @classmethod
    def from_llm(cls, llm: LLM...Assessment) -> "...Assessment":
        return cls.model_validate(llm.model_dump())
```

Die bestehenden Markdown-Dateien in

```text
smi/data/schema/optimisation_potential
smi/data/schema/sub_optimisation_potential
```

beschreiben fachlich, welche Pydantic-Schemas zu erstellen sind. Lies diese Dateien und leite daraus sinnvolle strukturierte Schemas ab.

Bewertungslogik:
Implementiere eine einfache Aggregationslogik für das Gesamtergebnis eines übergeordneten Optimierungspotenzials aus den Ratings der Subpotenziale:

```text
Wenn mindestens ein Subpotenzial high ist  -> Gesamtbewertung high
Sonst wenn mindestens ein Subpotenzial medium ist -> Gesamtbewertung medium
Sonst -> Gesamtbewertung low
```

Die Logik soll aus der fachlichen Beschreibung in

```text
smi/data/schema/optimisation_potential/1_potential.md
```

abgeleitet und einfach implementiert werden.

Prozess:

1. Initialisierung

* Lade `.env`.
* Erzeuge das ChatModel über die bestehende Factory.
* Lade:

  * Bild anhand `sheet_metal_id`
  * Prüfplan-PDF pro übergeordnetem Optimierungspotenzial
  * Basis-Prompt aus `smi/data/schema/1_prompt.md`
  * Schema-/Beschreibungsdaten der übergeordneten und untergeordneten Optimierungspotenziale

2. Bewertung der Sub-Optimierungspotenziale
   Für jedes ausgewählte übergeordnete Optimierungspotenzial:

* Ermittle alle zugehörigen Sub-Optimierungspotenziale.
* Führe für jedes Subpotenzial einen unabhängigen LLM-Aufruf aus.
* Jeder LLM-Aufruf bekommt:

  * Bild der Blechkonstruktion
  * vollständige Prüfplan-PDF
  * Basis-Prompt
  * fachliche Beschreibung des übergeordneten Optimierungspotenzials
  * fachliche Beschreibung des jeweiligen Sub-Optimierungspotenzials
  * LLM-Antwortschema

Die Aufrufe sollen gesammelt per `abatch` ausgeführt werden.
Setze `max_concurrency` aus `LLM_MAX_CONCURRENCY`.

Nutze für Bild-Inputs das LangChain-Format mit `HumanMessage` und multimodalem Content.
Lokale Bilder sollen als Base64/Data-URL eingebettet werden.

3. Aggregation

* Aggregiere die Bewertungen der Subpotenziale je übergeordnetem Optimierungspotenzial.
* Nutze die einfache `low` / `medium` / `high`-Logik.
* Erzeuge ein Application-Ergebnisobjekt für den Report.

4. HTML-Report
   Erzeuge ausschließlich einen HTML-Report.

Speicherort:

```text
smi/output/reports/{sheet_metal_id}_{timestamp}.html
```

Der Report soll enthalten:

* Bild der Blechkonstruktion ganz oben, eingebettet als Base64
* Übersicht der geprüften übergeordneten Optimierungspotenziale
* Je übergeordnetem Optimierungspotenzial:
  * Wichtige Attribute, entscheide selbständig welche Attribute aus den Schemas relevant für den Report sind und wie du sie im Report anordnest 
* Je Sub-Optimierungspotenzial:
  * Wichtige Attribute, entscheide selbständig welche Attribute aus den Schemas relevant für den Report sind und wie du sie im Report anordnest 
* Modernes, minimalistisches Design
* Farbige Badges für Ratings:

  * `low`
  * `medium`
  * `high`
* Der Report soll übersichtlich bleiben, aber alle wesentlichen Informationen enthalten.

Fehlerbehandlung und Logging:

* Nutze `logging`.
* Wenn ein einzelner LLM-Aufruf fehlschlägt, soll nicht der ganze Prozess abbrechen.
* Verwende bei `abatch` `return_exceptions=True`.
* Logge Fehler mit Kontext:

  * `sheet_metal_id`
  * `optimisation_potential_id`
  * `sub_optimisation_potential_id`
  * `model_name`
* Erfolgreiche Bewertungen sollen weiterverarbeitet werden.

Akzeptanzkriterien:

* Das Script kann mit `sheet_metal_id="SM01"` und `optimisation_potential_ids=["P01"]` gestartet werden.
* Das Bild wird aus `smi/data/kb/sm/SM01.png` geladen.
* Der Prüfplan `smi/data/optimisation_potential/P01.pdf` wird vollständig an das LLM übergeben.
* Alle zugehörigen Sub-Optimierungspotenziale von `P01` werden unabhängig bewertet.
* Die LLM-Antworten werden per Pydantic validiert.
* LLM-Schemas und Application-Schemas sind sauber getrennt.
* Die Bewertung läuft asynchron per `abatch` mit Concurrency-Limit.
* Das Gesamtergebnis wird aus den Sub-Ratings aggregiert.
* Ein HTML-Report wird unter `smi/output/reports` erzeugt.
* Das Bild ist im HTML-Report eingebettet.
* Das Projekt ist minimalistisch, verständlich und vollständig in Markdown dokumentiert.
* Die Dokumentation erklärt:

  * Ziel der Anwendung
  * Konfiguration
  * Datenstruktur
  * Ausführung
  * Bewertungslogik
  * Report-Erzeugung

Bitte implementiere die Lösung vollständig und halte den Code einfach, lesbar und konsistent.

```

