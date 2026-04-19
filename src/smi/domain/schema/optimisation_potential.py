"""Schemas for an aggregated optimisation-potential assessment."""

from collections.abc import Iterable
from enum import Enum

from pydantic import BaseModel, ConfigDict

from smi.domain.schema.sub_optimisation_potential import (
    Rating,
    SubPotentialAssessment,
)


class OverallRating(str, Enum):
    """Aggregated rating for a parent potential."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    NONE = "none"


def aggregate_rating(subs: Iterable[SubPotentialAssessment]) -> OverallRating:
    """Aggregate sub-ratings: any high → high, else any medium → medium, else low.

    Sub-potentials that failed (``error`` set) do not contribute to the rating.
    If no successful sub-assessment exists, returns ``NONE``.
    """
    successful = [s for s in subs if s.error is None]
    if not successful:
        return OverallRating.NONE
    if any(s.rating is Rating.HIGH for s in successful):
        return OverallRating.HIGH
    if any(s.rating is Rating.MEDIUM for s in successful):
        return OverallRating.MEDIUM
    return OverallRating.LOW


class OptimisationPotentialAssessment(BaseModel):
    """Application-level result for one parent optimisation potential."""

    model_config = ConfigDict(extra="forbid")

    potential_id: str
    potential_name: str
    subpotentials: list[SubPotentialAssessment]
    rating: OverallRating
