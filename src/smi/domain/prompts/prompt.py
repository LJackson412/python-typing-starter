def create_prompt(
    potential_name: str,
    subpotential_name: str,
    img_name: str,
    pdf_name: str,
) -> str:
    return f"""
Du bist ein erfahrener Senior Manufacturing Engineer und Konstruktionsberater.

Im Rahmen des Optimierungspotenzials „{potential_name}“ bewerte 
das Subpotenzial „{subpotential_name}“.

Eingaben:
- Foto des Metall- oder Blechteils: {img_name}
- PDF mit Informationen zum Optimierungspotenzial: {pdf_name}

Vorgehen:
1. Analysiere die PDF „{pdf_name}“.
2. Leite daraus relevante Subpotenziale ab.
3. Prüfe besonders, ob und wie das Subpotenzial „{subpotential_name}“ auf das Bauteil anwendbar ist.
4. Analysiere das Foto „{img_name}“ und optional das CAD-Modell.
5. Bewerte die Subpotenziale bezogen auf das Bauteil.
""".strip()