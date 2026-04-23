from ast import Return
from enum import Enum, auto


class ErrorCode(Enum):
    SUCCESS = 0
    NONE = auto()

    # Generate
    ERROR_MISSING_INPUT = auto()

    # Displacer
    ERROR_DISPLACER_ADMIN_MISSING = auto()
    ERROR_DISPLACER_AREA_MISSING = auto()
    ERROR_DISPLACER_NUMBER_MISSING = auto()
    ERROR_DISPLACER_CLUSTER_OUTSIDE_BOUNDARY = auto()
    ERROR_DISPLACER_CLUSTER_DISPLACED_OUTSIDE_GEODOMAIN = auto()
    ERROR_DISPLACER_CLUSTER_ADMIN_CONFLICT_ADMIN_GEOMETRY = auto()
    ERROR_DISPLACER_URBANISM_CONSTRAINT_VIOLATED = auto()
    ERROR_DISPLACER_ORIGINAL_POINT_IN_WATER = auto()
    ERROR_DISPLACER_ORIGINAL_POINT_IN_NOT_VALID_CLASS = auto()


ErrorDisplayString = {
    ErrorCode.SUCCESS: "",
    ErrorCode.NONE: "Null",

    ErrorCode.ERROR_DISPLACER_ADMIN_MISSING: "Admin boundary is missing from cluster source",
    ErrorCode.ERROR_DISPLACER_AREA_MISSING: "Area type is missing",
    ErrorCode.ERROR_DISPLACER_NUMBER_MISSING: "Cluster number is missing",
    ErrorCode.ERROR_DISPLACER_CLUSTER_DISPLACED_OUTSIDE_GEODOMAIN: "Cluster was displaced in another geodomain",
    ErrorCode.ERROR_DISPLACER_CLUSTER_ADMIN_CONFLICT_ADMIN_GEOMETRY: "Cluster's admin name does not match with Admin geometry",
    ErrorCode.ERROR_DISPLACER_CLUSTER_OUTSIDE_BOUNDARY: "Cluster is outside the boundary shapefile",
    ErrorCode.ERROR_DISPLACER_URBANISM_CONSTRAINT_VIOLATED: "Displaced point violates urbanism class group constraint",
    ErrorCode.ERROR_DISPLACER_ORIGINAL_POINT_IN_WATER: "Original centroid is located in water body (class 10)",
    ErrorCode.ERROR_DISPLACER_ORIGINAL_POINT_IN_NOT_VALID_CLASS: "Original centroid is located in non valid class"
}
