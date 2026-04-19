from dataclasses import dataclass, field
from enum import Enum
from typing import Type

from pydantic import BaseModel, Field, ConfigDict


class CheckpointTyp(str, Enum):
    QUANTITATIV = "quantitativ"
    QUALITATIV = "qualitativ"


class Rating(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LLMPotenzialRatingLogic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    high: str = Field(..., description="Bedingung für hohes Potenzial")
    medium: str = Field(..., description="Bedingung für mittleres Potenzial")
    low: str = Field(..., description="Bedingung für geringes Potenzial")


class LLMSheetMetalSubPotentialResult(BaseModel):
    """
    Das ist ausschließlich das erwartete LLM-Ergebnis.
    Diese Felder sollen vom LLM befüllt werden.
    """

    model_config = ConfigDict(extra="forbid")

    rating: Rating = Field(
        ...,
        description="Bewertung des Subpotentials anhand der vorgegebenen Rating-Logik",
    )
    reason: str = Field(
        ...,
        description="Technische Begründung der Bewertung auf Basis beobachtbarer Hinweise",
    )
    evidence: list[str] = Field(
        ...,
        description="Beobachtbare Hinweise aus Bild, CAD oder Abwicklung",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Sicherheit der Bewertung abhängig von Vollständigkeit und Qualität der Eingabedaten",
    )


@dataclass(frozen=True, slots=True)
class SheetMetalSubPotential:
    """
    Statische Definition eines Blech-Subpotentials.

    Diese Daten sind vor der LLM-Auswertung bekannt und werden
    als Kontext / Instruktion in den Prompt gegeben.
    """

    subpotential_id: str = field(
        metadata={
            "description": "Eindeutige ID des Subpotentials",
        }
    )

    subpotential_name: str = field(
        metadata={
            "description": "Name des Subpotentials",
        }
    )

    checkpoint_typ: CheckpointTyp = field(
        metadata={
            "description": "Gibt an, ob die Bewertung zahlenbasiert oder qualitativ erfolgt",
        }
    )

    llm_evaluation_goal: str = field(
        metadata={
            "description": "Beschreibt dem LLM das Ziel der Bewertung",
        }
    )

    llm_check_method: str = field(
        metadata={
            "description": "Gibt dem LLM vor, wie das Subpotential zu bewerten ist",
        }
    )

    llm_potenzial_rating_logic: LLMPotenzialRatingLogic = field(
        metadata={
            "description": "Rating-Logik zur Bewertung des Subpotentials",
        }
    )

    llm_result_model: Type[BaseModel] = field(
        default=LLMSheetMetalSubPotentialResult,
        metadata={
            "description": "Pydantic-Modell für das erwartete LLM-Ergebnis",
        },
    )