from dataclasses import dataclass, field
from enum import Enum

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

    high: str = Field(
        ...,
        description="Bedingung für hohes Potenzial",
    )
    medium: str = Field(
        ...,
        description="Bedingung für mittleres Potenzial",
    )
    low: str = Field(
        ...,
        description="Bedingung für geringes Potenzial",
    )


class LLMSheetMetalSubPotential(BaseModel):
    """
    Pydantic-Modell für alle Felder, die vom LLM verwendet,
    bewertet oder als Ergebnis geliefert werden.
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
        description="Beobachtbare Hinweise aus dem Bild der Blechkonstruktion",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Sicherheit der Bewertung abhängig von Vollständigkeit und Qualität der Eingabedaten",
    )


@dataclass
class SheetMetalSubPotential:
    """
    Dataclass für ein generisches Blech-Sub-Potenzial.
    Enthält die nicht vom LLM zu befüllenden Metadaten sowie
    das Pydantic-Modell mit den LLM-relevanten Feldern.
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

    # following are used in the system prompt
    llm_model: type[LLMSheetMetalSubPotential] = field(
        default=LLMSheetMetalSubPotential,
        metadata={
            "description": "Pydantic-Modell mit LLM-Bewertungs- und LLM-Ergebnisfeldern",
        },
    )
    llm_evaluation_goal: str = Field(
        metadata={
            "description": "Beschreibt das Ziel der Bewertung",
        }
    )
    llm_check_method: str = Field(
        metadata={
            "description": "Gibt dem LLM vor, wie das Subpotential zu bewerten ist",
        }
    )
    llm_potenzial_rating_logic: LLMPotenzialRatingLogic = Field(
        metadata={
            "description": "Rating-Logik zur Bewertung des Subpotentials",
        }
    )