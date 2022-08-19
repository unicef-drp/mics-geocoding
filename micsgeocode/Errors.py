from ast import Return
from enum import Enum, auto


class ErrorCode(Enum):
    SUCCESS = 0
    NONE = auto()

    # Displacer
    ERROR_DISPLACER_ADMIN_MISSING = auto()
    ERROR_DISPLACER_AREA_MISSING = auto()
    ERROR_DISPLACER_NUMBER_MISSING = auto()
    ERROR_DISPLACER_CLUSTER_OUTSIDE_BOUNDARY = auto()
    ERROR_DISPLACER_CLUSTER_DISPLACED_OUTSIDE_GEODOMAIN = auto()


ErrorDisplayString = {
    ErrorCode.SUCCESS: "",
    ErrorCode.NONE: "Null",

    ErrorCode.ERROR_DISPLACER_ADMIN_MISSING: "Admin boundary is missing from cluster source",
    ErrorCode.ERROR_DISPLACER_AREA_MISSING: "Area type is missing",
    ErrorCode.ERROR_DISPLACER_NUMBER_MISSING: "Cluster number is missing",
    ErrorCode.ERROR_DISPLACER_CLUSTER_DISPLACED_OUTSIDE_GEODOMAIN: "Cluster was displaced in another geodomain",
    ErrorCode.ERROR_DISPLACER_CLUSTER_OUTSIDE_BOUNDARY: "Cluster is outside the boundary shapefile"
}
