"""Laufzeit-ViewModels für LLM-Bewertungsergebnisse.

Trennt bewusst statische Definitionen (siehe
``smi.domain.schema.sub_potential``/``potential``) von Laufzeitdaten, die nach
einem LLM-Aufruf anfallen.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from smi.domain.schema.potential import PotentialRating
from smi.domain.schema.sub_potential import (
    CheckpointTyp,
    LLMSheetMetalSubPotential,
    Rating,
    SheetMetalSubPotential,
)


class SubPotentialResult(BaseModel):
    """Ergebnis eines einzelnen Subpotenzial-Aufrufs."""

    model_config = ConfigDict(extra="forbid")

    subpotential_id: str
    subpotential_name: str
    checkpoint_typ: CheckpointTyp
    rating: Rating
    reason: str
    evidence: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    error: str | None = Field(
        default=None,
        description="Gesetzt, wenn der LLM-Call eine Exception geworfen hat.",
    )

    @classmethod
    def from_llm(
        cls,
        *,
        spec: SheetMetalSubPotential,
        llm: LLMSheetMetalSubPotential,
    ) -> "SubPotentialResult":
        """Mappt LLM-Antwort + statische Metadaten auf ein Ergebnis."""
        return cls(
            subpotential_id=spec.subpotential_id,
            subpotential_name=spec.subpotential_name,
            checkpoint_typ=spec.checkpoint_typ,
            rating=llm.rating,
            reason=llm.reason,
            evidence=list(llm.evidence),
            confidence=llm.confidence,
            error=None,
        )

    @classmethod
    def from_error(
        cls,
        *,
        spec: SheetMetalSubPotential,
        exc: BaseException,
    ) -> "SubPotentialResult":
        """Fallback-Ergebnis bei gefangener Exception aus ``abatch``.

        Rating wird auf ``LOW`` / ``confidence=0.0`` gesetzt, damit die
        Aggregation zwar einen Wert erhält, das Ergebnis aber im Report
        eindeutig als Fehler ausgewiesen werden kann (``error`` != None).
        """
        return cls(
            subpotential_id=spec.subpotential_id,
            subpotential_name=spec.subpotential_name,
            checkpoint_typ=spec.checkpoint_typ,
            rating=Rating.LOW,
            reason="LLM-Aufruf fehlgeschlagen.",
            evidence=[],
            confidence=0.0,
            error=f"{type(exc).__name__}: {exc}",
        )


class PotentialResult(BaseModel):
    """Aggregiertes Ergebnis eines übergeordneten Optimierungspotenzials."""

    model_config = ConfigDict(extra="forbid")

    potential_id: str
    potential_name: str
    rating: PotentialRating
    subpotentials: list[SubPotentialResult]
