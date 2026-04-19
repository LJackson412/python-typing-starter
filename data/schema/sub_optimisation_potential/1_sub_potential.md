## Generisches Blech-Sub-Potenzial-Schema  

| Attribut                        | Typ / Struktur                     | Befüllung     | Beschreibung                                                                          |
| ------------------------------- | ---------------------------------- | ------------- | ------------------------------------------------------------------------------------- |
| `subpotential_id`               | String                             | Kein LLM      | - Eindeutige ID des Subpotentials                                                     |
| `subpotential_name`             | String                             | Kein LLM      | - Name des Subpotentials                                                              |
| `checkpoint_typ`                | Enum: `quantitativ` / `qualitativ` | Kein LLM      | - Gibt an, ob die Bewertung zahlenbasiert oder qualitativ erfolgt                     |
| `evaluation_goal`               | String                             | LLM-Bewertung | - Beschreibt das Ziel der Bewertung                                                   |
| `check_method`                  | String                             | LLM-Bewertung | - Gibt dem LLM vor, wie das Subpotential zu bewerten ist                              |
| `potenzial_rating_logic.high`   | String                             | LLM-Bewertung | - Bedingung für hohes Potenzial                                                       |
| `potenzial_rating_logic.medium` | String                             | LLM-Bewertung | - Bedingung für mittleres Potenzial                                                   |
| `potenzial_rating_logic.low`    | String                             | LLM-Bewertung | - Bedingung für geringes Potenzial                                                    |
| `rating`                        | Enum: `high` / `medium` / `low`    | LLM-Ergebnis  | - Bewertung des Subpotentials anhand der vorgegebenen Rating-Logik                    |
| `reason`                        | String                             | LLM-Ergebnis  | - Technische Begründung der Bewertung auf Basis beobachtbarer Hinweise                |
| `evidence`                      | String-Liste                       | LLM-Ergebnis  | - Beobachtbare Hinweise aus Bild, CAD oder Abwicklung                                 |
| `confidence`                    | Float `0.0–1.0`                    | LLM-Ergebnis  | - Sicherheit der Bewertung abhängig von Vollständigkeit und Qualität der Eingabedaten |


