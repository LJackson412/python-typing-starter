"""Registry der bekannten Optimierungspotenziale (P-Ebene)."""

from __future__ import annotations

from smi.domain.potentials.definitions import P01_REDUCE_PART_COUNT
from smi.domain.schema.potential import SheetMetalPotential

POTENTIAL_REGISTRY: dict[str, SheetMetalPotential] = {
    P01_REDUCE_PART_COUNT.potential_id: P01_REDUCE_PART_COUNT,
}


def get_potential(potential_id: str) -> SheetMetalPotential:
    """Liefert die statische Definition zu einer Potenzial-ID.

    Wirft ``KeyError`` mit klarer Meldung, falls die ID unbekannt ist.
    """
    try:
        return POTENTIAL_REGISTRY[potential_id]
    except KeyError as exc:
        known = ", ".join(sorted(POTENTIAL_REGISTRY)) or "<keine>"
        raise KeyError(
            f"Unbekannte potential_id: {potential_id!r} (bekannt: {known})"
        ) from exc
