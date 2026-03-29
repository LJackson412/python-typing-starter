--

name: api-review

description: Verwende diesen Skill, wenn API-Design, Endpunkte, Request-/Response-Schemas oder Breaking Changes geprüft werden sollen.

---

## Ziel

Sichere, konsistente Prüfung von API-Änderungen.

## Vorgehen

1. Erfasse betroffene Endpunkte und Datenmodelle.

2. Prüfe Benennung, Statuscodes und Fehlerobjekte.

3. Beurteile Backward Compatibility.

4. Suche nach fehlenden Beispielen für Requests und Responses.

5. Gib ein kurzes Review mit Befunden und Empfehlungen aus.

## Beachte

- Bei öffentlichen APIs Breaking Changes ausdrücklich markieren.

- Bei Unsicherheit Beispiele aus `references/examples.md` heranziehen.