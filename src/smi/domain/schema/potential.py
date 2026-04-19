# smi/domain/schema/potential.py

from dataclasses import dataclass, field
from enum import Enum

from smi.domain.schema.sub_potential import SheetMetalSubPotential


class PotentialRating(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


@dataclass(frozen=True, slots=True)
class SheetMetalPotential:
    """
    Statische Definition eines übergeordneten Blech-Potentials.

    Diese Daten werden nicht durch das LLM befüllt.
    Die Bewertung des Potentials wird später aus den Bewertungen
    der enthaltenen Subpotentials berechnet.
    """

    potential_id: str = field(
        metadata={
            "description": "Eindeutige ID des übergeordneten Potentials",
        }
    )

    potential_name: str = field(
        metadata={
            "description": "Name des übergeordneten Optimierungspotentials",
        }
    )

    subpotentials: tuple[SheetMetalSubPotential, ...] = field(
        metadata={
            "description": "Zugehörige statische Subpotential-Definitionen",
        }
    )

    rating: PotentialRating = field(
        default=PotentialRating.NONE,
        metadata={
            "description": "Berechnete Gesamtbewertung aus den enthaltenen Subpotentials",
        },
    )