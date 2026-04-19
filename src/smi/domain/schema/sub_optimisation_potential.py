"""Schemas for a single sub-optimisation-potential assessment."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Rating(str, Enum):
    """Rating an LLM assigns to a single sub-potential."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LLMSubPotentialAssessment(BaseModel):
    """Exact fields the LLM fills in via structured output."""

    model_config = ConfigDict(extra="forbid")

    rating: Rating = Field(
        description="Bewertung gemäß der Rating-Logik des Subpotenzials."
    )
    reason: str = Field(
        description="Knappe technische Begründung der Bewertung auf Basis "
        "beobachtbarer Hinweise aus Bild und PDF.",
    )
    evidence: list[str] = Field(
        description="Liste konkreter beobachtbarer Hinweise aus Bild, CAD "
        "oder Abwicklung, die das Rating stützen.",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Sicherheit der Bewertung (0.0 = unsicher, 1.0 = sicher).",
    )


class SubPotentialAssessment(BaseModel):
    """Application-level assessment: LLM result plus static metadata."""

    model_config = ConfigDict(extra="forbid")

    subpotential_id: str
    subpotential_name: str
    checkpoint_typ: Literal["quantitativ", "qualitativ"] | None = None
    rating: Rating
    reason: str
    evidence: list[str]
    confidence: float
    error: str | None = None

    @classmethod
    def from_llm(
        cls,
        llm: LLMSubPotentialAssessment,
        *,
        subpotential_id: str,
        subpotential_name: str,
        checkpoint_typ: Literal["quantitativ", "qualitativ"] | None,
    ) -> "SubPotentialAssessment":
        return cls(
            subpotential_id=subpotential_id,
            subpotential_name=subpotential_name,
            checkpoint_typ=checkpoint_typ,
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
        subpotential_id: str,
        subpotential_name: str,
        checkpoint_typ: Literal["quantitativ", "qualitativ"] | None,
        error: str,
    ) -> "SubPotentialAssessment":
        return cls(
            subpotential_id=subpotential_id,
            subpotential_name=subpotential_name,
            checkpoint_typ=checkpoint_typ,
            rating=Rating.LOW,
            reason="Bewertung fehlgeschlagen.",
            evidence=[],
            confidence=0.0,
            error=error,
        )
