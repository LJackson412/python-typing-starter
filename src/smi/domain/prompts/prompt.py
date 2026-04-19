def create_prompt(
    potential_name: str,
    subpotential_name: str,
    img_name: str,
    pdf_name: str,
    potential_high: str,
    potential_medium: str,
    potential_low: str
) -> str:
    return f"""
    Du bist ein erfahrener Senior Manufacturing Engineer, Konstruktionsberater und Experte
    im Bereich Blechproduktion. Dein Aufgabe ist es das Blechpotenzial einer Blechkonstruktion 
    anhand einer fest definierten Bewertungslogik zu bewerten. \n

    Im Rahmen des Optimierungspotenzials „{potential_name}“ bewerte 
    das Subpotenzial „{subpotential_name}“ nach der folgenden Bewertungslogik. \n

    Eingaben: \n
    - Foto des Metall- oder Blechteils: {img_name}
    - PDF mit Informationen zum Optimierungspotenzial: {pdf_name}\n

    Vorgehen: \n
    1. Analysiere die PDF „{pdf_name}“. \n
    2. Identifiziere relevante Informationen zu Bewertung von dem Subpotenzial „{subpotential_name}“\n
    4. Analysiere das Foto der Blechkonstruktion „{img_name}“.\n
    5. Leit Beobachtbare Hinweise aus dem Bild „{img_name}“ der Blechkonstruktion ab.\n
    5. Bewerte das Subpotenzial „{subpotential_name}“ nach der  Bewertungslogik.\n

    Bewertungslogik:\n\n
    Bedingung für hohes Potenzial:\n
    {potential_high}\n
    Bedingung für mittleres Potenzial:\n
    {potential_medium}\n
    Bedingung für geringes Potenzial:\n
    {potential_low}\n

    """.strip()