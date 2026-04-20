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

from pydantic import BaseModel, Field, ConfigDict, model_validator


class ImageMark(BaseModel):
    """
    Minimaler Bildmarker für einen Optimierungsbereich.

    Koordinatensystem:
    - x/y sind relative Bildkoordinaten von 0.0 bis 1.0
    - x=0.0 = linker Bildrand
    - x=1.0 = rechter Bildrand
    - y=0.0 = oberer Bildrand
    - y=1.0 = unterer Bildrand
    """

    model_config = ConfigDict(extra="forbid")

    optimization_area: str = Field(
        ...,
        description=(
            "Kurze Bezeichnung des markierten Optimierungsbereichs, "
            "z. B. '90°-Schweißverbindung', 'Zusatzteil integrieren', "
            "'mögliche Biegelinie', 'Bohrbild als Einschränkung'."
        ),
    )

    xMin: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Linke Grenze der Markierung, relativ zur Bildbreite.",
    )

    yMin: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Obere Grenze der Markierung, relativ zur Bildhöhe.",
    )

    xMax: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Rechte Grenze der Markierung, relativ zur Bildbreite.",
    )

    yMax: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Untere Grenze der Markierung, relativ zur Bildhöhe.",
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
    image_marks: list[ImageMark] = Field(
        default_factory=list,
        description=(
            """
            Optionale Bildmarkierungen für **relevante** Optimierungsbereiche.
            Wenn **kein** sinnvoller Optimierungsbereich im Bild markierbar ist, 
            muss diese Liste leer sein. Marker dienen dazu dem Nutzer **relevante** 
            Optimierungsbereiche für das Subpotenzial im Bild anzuzeigen.
            KOORDINATEN-REGELN für **ImageMark**:
            - x und y sind relative Koordinaten im Bild: 0.0 = linker/oberer Rand, 1.0 = rechter/unterer Rand
            - x=0.0 ist der LINKE Bildrand, x=1.0 ist der RECHTE Bildrand
            - y=0.0 ist der OBERE Bildrand, y=1.0 ist der UNTERE Bildrand
            - Stelle dir das Bild als 10x10 Raster vor: x=0.3 ist 3/10 von links, y=0.7 ist 7/10 von oben
            - Schaue dir das Bild genau an und identifiziere die Position des Optimierungsbereichs im Raster
            """
        ),
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