# ## Generisches Blech-Potenzial-Schema  

| Attribut         | Typ / Struktur                           | Befüllung                                                  | Beschreibung                                                                      |
| ---------------- | ---------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `potential_id`   | String                                   | Statisch / nicht durch LLM                                 | Eindeutige ID des übergeordneten Potenzials.                                      |
| `potential_name` | String                                   | Statisch / nicht durch LLM                                 | Name des übergeordneten Optimierungspotenzials.                                   |
| `subpotentials`  | Liste von Subpotential Cards             | Statisch + LLM-Ergebnisse innerhalb der Subpotential Cards | Enthält alle zugehörigen Subpotential Cards inklusive deren Bewertungsergebnisse. |
| `rating`         | Enum: `high` / `medium` / `low` / `none` | Berechnet / nicht durch LLM                                | Gesamtbewertung, abgeleitet aus den Ratings der enthaltenen Subpotentials.        |














