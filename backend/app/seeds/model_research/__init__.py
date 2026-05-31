from app.seeds.model_research.audi_a4_avant_b9 import (
    AUDI_A4_AVANT_B9_PROFILE,
    build_audi_a4_avant_b9_seed,
)
from app.seeds.model_research.bmw_320d_touring import (
    BMW_320D_TOURING_PROFILE,
    build_bmw_320d_touring_seed,
)

__all__ = [
    "AUDI_A4_AVANT_B9_PROFILE",
    "BMW_320D_TOURING_PROFILE",
    "VW_GOLF_VARIANT_MK7_PROFILE",
    "VW_PASSAT_GTE_VARIANT_PROFILE",
    "build_audi_a4_avant_b9_seed",
    "build_bmw_320d_touring_seed",
    "build_vw_golf_variant_mk7_seed",
    "build_vw_passat_gte_variant_seed",
]

from app.seeds.model_research.vw_passat_gte_variant import (
    VW_PASSAT_GTE_VARIANT_PROFILE,
    build_vw_passat_gte_variant_seed,
)

from app.seeds.model_research.vw_golf_variant_mk7 import (
    VW_GOLF_VARIANT_MK7_PROFILE,
    build_vw_golf_variant_mk7_seed,
)
