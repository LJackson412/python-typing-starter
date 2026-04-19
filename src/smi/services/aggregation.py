"""Aggregation von Subpotenzial-Bewertungen zu einem Gesamtrating."""

from __future__ import annotations

from collections.abc import Iterable

from smi.domain.schema.potential import PotentialRating
from smi.domain.schema.result import SubPotentialResult
from smi.domain.schema.sub_potential import Rating


def aggregate_rating(subs: Iterable[SubPotentialResult]) -> PotentialRating:
    """Bestimmt das Gesamtrating eines Potenzials aus seinen Subpotenzialen.

    Regel: ``high`` schlägt ``medium`` schlägt ``low``. Fehler-Ergebnisse
    (``error`` gesetzt) werden ignoriert. Bleibt nach Filter nichts übrig,
    ergibt sich ``none``.
    """
    valid = [s for s in subs if s.error is None]
    if not valid:
        return PotentialRating.NONE
    if any(s.rating is Rating.HIGH for s in valid):
        return PotentialRating.HIGH
    if any(s.rating is Rating.MEDIUM for s in valid):
        return PotentialRating.MEDIUM
    return PotentialRating.LOW
