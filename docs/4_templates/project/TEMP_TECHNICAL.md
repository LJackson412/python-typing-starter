# Template 2 — OnePager: Technischer Überblick (adaptiv, je nach Anwendung)

> Zweck: Für PO, Team, Stakeholder, technische Kundenansprache oder interne Architekturübersicht.  
> Fokus: Kontext, Schnittstellen, Container, Deployment sowie relevante Risiken und Entscheidungen.  
> Wichtig: Die Bereiche unten sind absichtlich nicht „in Stein gemeißelt“. Nutze nur die Abschnitte, die für die konkrete Anwendung wirklich relevant sind.

---

## [PROJEKTNAME / SYSTEMNAME] — Technischer Überblick

**Technische Kurzbeschreibung:**  
[1–2 Sätze zur Architekturidee, zum Systemzweck und zur Betriebsform.]

**Technische Einordnung:**  
- **Systemtyp:** [z. B. SaaS, internes Tool, Plattform, API-first, Multi-Tenant]
- **Betriebsmodell:** [z. B. Cloud, On-Prem, Hybrid]
- **Nutzergruppen:** [z. B. Endnutzer, Admins, Support, Fremdsysteme]
- **Reifegrad:** [z. B. Idee, MVP, Pilot, produktiv]

---

## 1. System Context Diagram (C4)

**Ziel:** Zeigt Nutzer, dein SaaS und externe Systeme im Gesamtkontext.

**Diagramm-Platzhalter:**  
![Platzhalter: C4 System Context Diagram](./placeholder-system-context.png)

**Kurzbeschreibung des Kontexts:**  
- **Nutzer / Akteure:** [Wer interagiert direkt mit dem System?]
- **Dein SaaS / Kernsystem:** [Was ist die zentrale Verantwortung?]
- **Externe Systeme:** [Welche Systeme sind angebunden?]
- **Kommunikationsbeziehungen:** [Wie kommunizieren die Beteiligten?]

**Beispielhafte Elemente:**  
- [Web-App / Mobile App / Admin-Portal]
- [Identity Provider]
- [ERP / CRM / Drittsystem]
- [Benachrichtigungsdienst]
- [Analytics / Logging / Monitoring]

---

## 2. Integrationen & Datenflüsse

> Diesen Abschnitt flexibel halten. Je nach Anwendung stehen APIs, Events, Dateien, Identitäten, Abrechnungsdaten oder Audit-Daten im Vordergrund.

**Integrationsübersicht:**  

| Integration / System | Richtung | Daten / Ereignisse | Protokoll / Mechanismus | Relevanz |
|---|---|---|---|---|
| [System A] | [ein/aus/beides] | [z. B. Nutzerdaten, Aufträge, Events] | [REST, GraphQL, Webhook, SFTP, Queue] | [hoch/mittel/niedrig] |
| [System B] | [ein/aus/beides] | [Beschreibung] | [Beschreibung] | [Beschreibung] |
| [System C] | [ein/aus/beides] | [Beschreibung] | [Beschreibung] | [Beschreibung] |

**Datenfluss-Grafik:**  
![Platzhalter: Integrations- / Datenflussdiagramm](./placeholder-dataflow.png)

**Wichtige Fragen zur Konkretisierung:**  
- Welche Datenobjekte sind geschäftskritisch?  
- Welche Daten werden gespeichert, synchronisiert oder nur durchgeleitet?  
- Gibt es synchrone und asynchrone Flüsse?  
- Wo entstehen Abhängigkeiten, Latenzen oder Fehlerszenarien?  
- Welche Sicherheits- oder Compliance-Anforderungen gelten für diese Daten?

---

## 3. System Context + Container Diagram (C4)

> Dieser Abschnitt kann sehr kompakt oder detaillierter ausfallen.  
> Sinnvoll, wenn intern verstanden werden soll, welche Hauptbausteine existieren und wie sie zusammenarbeiten.

**Diagramm-Platzhalter:**  
![Platzhalter: C4 Container Diagram](./placeholder-container-diagram.png)

**Container / Hauptbausteine:**  

| Container / Baustein | Verantwortung | Technologie / Plattform | Schnittstellen |
|---|---|---|---|
| [Frontend] | [UI, Interaktion, Darstellung] | [z. B. React, Vue] | [z. B. REST API] |
| [Backend / API] | [Business-Logik] | [z. B. Node.js, Java, .NET] | [Beschreibung] |
| [Datenbank] | [Persistenz] | [z. B. PostgreSQL] | [Beschreibung] |
| [Worker / Jobs] | [Asynchrone Verarbeitung] | [z. B. Queue Worker] | [Beschreibung] |
| [Auth / IAM] | [Authentifizierung / Autorisierung] | [z. B. Keycloak, Auth0] | [Beschreibung] |

**Optional ergänzen:**  
- [Caching]
- [Search]
- [Event Bus / Messaging]
- [Reporting]
- [File Storage]
- [Observability-Komponenten]

---

## 4. Deployment-View

> Nur die tatsächlich relevanten Ebenen zeigen. Bei manchen Systemen reicht eine stark vereinfachte Sicht.

**Deployment-Diagramm-Platzhalter:**  
![Platzhalter: Deployment View](./placeholder-deployment-view.png)

**Betriebs- / Infrastrukturübersicht:**  
- **Umgebungen:** [Dev / Test / Staging / Prod]
- **Hosting:** [Cloud-Anbieter / Rechenzentrum / Hybrid]
- **Auslieferung:** [CI/CD, manuell, Container, Serverless]
- **Skalierung:** [horizontal, vertikal, auto-scaling, nicht relevant]
- **Verfügbarkeit / Resilienz:** [z. B. Single Region, Multi-AZ, Backup-Konzept]
- **Security-Grundlagen:** [z. B. IAM, Secrets, Netzwerkgrenzen, Verschlüsselung]

**Optional je nach Anwendung:**  
- Mandantenfähigkeit / Tenant-Isolation  
- Regionen / Datenresidenz  
- Backup / Restore  
- Release-Strategie  
- Observability / Monitoring / Alerting  
- Performance-Hotspots  
- Kostenrelevante Architekturtreiber  

---

## 5. Abhängigkeiten / Risiken / Entscheidungen

### Abhängigkeiten
- [Abhängigkeit 1: z. B. externer API-Anbieter]
- [Abhängigkeit 2: z. B. internes Plattform-Team]
- [Abhängigkeit 3: z. B. Auth-/IAM-System]

### Risiken
- [Risiko 1: z. B. Performance unter Last]
- [Risiko 2: z. B. instabile Fremdschnittstelle]
- [Risiko 3: z. B. regulatorische Anforderungen]
- [Risiko 4: z. B. unklare Datenverantwortung]

### Wichtige Entscheidungen / ADR-Light
| Entscheidung | Status | Begründung | Auswirkungen |
|---|---|---|---|
| [Entscheidung 1] | [offen/getroffen] | [Warum?] | [Konsequenz] |
| [Entscheidung 2] | [offen/getroffen] | [Warum?] | [Konsequenz] |
| [Entscheidung 3] | [offen/getroffen] | [Warum?] | [Konsequenz] |

---

## 6. Optionaler Baukasten für projektspezifische Schwerpunkte

> Die folgenden Blöcke nur dann ergänzen, wenn sie für die konkrete Anwendung entscheidend sind.

### A. Sicherheit & Compliance
- [Authentifizierung / SSO]
- [Autorisierung / Rollenmodell]
- [Verschlüsselung]
- [Audit Logging]
- [DSGVO / regulatorische Anforderungen]

### B. Datenmodell / Domänenobjekte
- [Wichtigste Entitäten]
- [Kritische Beziehungen]
- [Lifecycle / Ownership]

### C. Nichtfunktionale Anforderungen
- [Performance]
- [Verfügbarkeit]
- [Skalierbarkeit]
- [Wartbarkeit]
- [Beobachtbarkeit]

### D. Betriebsprozesse
- [Incident Handling]
- [Release-Prozess]
- [Rollback]
- [Support / Ownership]

### E. Technische Schulden / offene Architekturthemen
- [Thema 1]
- [Thema 2]
- [Thema 3]

---

## 7. Kurzfazit / Nächste Schritte

**Aktueller technischer Fokus:**  
[Was ist architektonisch oder technisch als Nächstes am wichtigsten?]

**Empfohlene nächsten Schritte:**  
- [Schritt 1]
- [Schritt 2]
- [Schritt 3]

**Verantwortlich / Ansprechpartner:**  
[Name, Rolle, Team]