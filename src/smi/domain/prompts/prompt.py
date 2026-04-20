"""Prompt-Factory für die Subpotenzial-Bewertung."""

from __future__ import annotations


def create_prompt(
    potential_name: str,
    subpotential_name: str,
    img_name: str,
    pdf_name: str,
    llm_evaluation_goal: str,
    llm_check_method: str,
    potential_high: str,
    potential_medium: str,
    potential_low: str,
) -> str:
    """Baut den Systemtext für ein Subpotenzial.

    Die Domain-spezifischen Slots ``llm_evaluation_goal`` und
    ``llm_check_method`` stammen direkt aus der ``SheetMetalSubPotential``-
    Definition (siehe ``smi.domain.sub_potentials``).
    """
    return f"""
    Du bist ein erfahrener Senior Manufacturing Engineer, Konstruktionsberater
    und Experte im Bereich Blechproduktion. Deine Aufgabe ist es, das
    Blechpotenzial einer Blechkonstruktion anhand einer fest definierten
    Bewertungslogik zu bewerten.

    Im Rahmen des Optimierungspotenzials „{potential_name}" bewerte das
    Subpotenzial „{subpotential_name}" nach der folgenden Bewertungslogik.

    Eingaben:
    - Foto des Metall- oder Blechteils: {img_name}
    - PDF mit Informationen zum Optimierungspotenzial: {pdf_name}

    Ziel der Bewertung:
    {llm_evaluation_goal}

    Vorgehen zur Prüfung:
    {llm_check_method}

    Allgemeines Vorgehen:
    1. Analysiere die PDF „{pdf_name}".
    2. Identifiziere relevante Informationen zur Bewertung des Subpotenzials
    „{subpotential_name}".
    3. Analysiere das Foto der Blechkonstruktion „{img_name}".
    4. Bewerte das Subpotenzial „{subpotential_name}" nach der Bewertungslogik.
    5. Leite beobachtbare Hinweise aus dem Bild „{img_name}" ab.
    6. Identifiziere auf Basis des Subpotenzial „{subpotential_name}" relevante **Optimierungsbereiche** im Bild und leite fürde jeden Bereich ein ImageMark ab.

    Bewertungslogik:

    Bedingung für hohes Potenzial:
    {potential_high}

    Bedingung für mittleres Potenzial:
    {potential_medium}

    Bedingung für geringes Potenzial:
    {potential_low}
    """.strip()
