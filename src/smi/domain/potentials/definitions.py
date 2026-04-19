from smi.domain.schema.potential import SheetMetalPotential
from smi.domain.sub_potentials.p01_definitions import (
    SP01_01_REPLACE_WELD_WITH_BEND,
    SP02_01_CHANGE_GEOMETRY_INTEGRATE_ADDITIONAL_PART,
)

P01_REDUCE_PART_COUNT = SheetMetalPotential(
    potential_id="P01",
    potential_name="Teile-/Bauteilanzahl reduzieren",
    subpotentials=(
        SP01_01_REPLACE_WELD_WITH_BEND,
        SP02_01_CHANGE_GEOMETRY_INTEGRATE_ADDITIONAL_PART,
    ),
)   