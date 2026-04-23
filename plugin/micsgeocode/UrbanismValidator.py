## ###########################################################################
##
# UrbanismValidator.py
##
# Author: M.Moreno
# Created: 19/9/2025
##
# Description: Handles urbanism raster validation for centroid displacement
##
# IMPORTANT: DEGURBA restriction is currently under review and not part of any release. It should not be considered as any official feature.
##
## ###########################################################################
import typing
from qgis.core import QgsGeometry, QgsRasterLayer, QgsPointXY, QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from .Logger import Logger
from . import Errors

class UrbanismValidator:
    """Validates displacement constraints based on urbanism raster classification"""

    # Class group definitions
    GROUP_1_CLASSES = [21, 22, 23, 30]  # Urban classes
    GROUP_2_CLASSES = [11, 12, 13]      # Rural classes  
    WATER_CLASS = 10                    # Water body - invalid

    def __init__(self):
        self.rasterLayer = None
        self.enabled = False

    def setRasterFile(self, rasterFile: str) -> bool:
        """Set urbanism raster file and validate it"""
        self.rasterLayer = QgsRasterLayer(rasterFile, "urbanism_restriction")
        self.enabled = self.rasterLayer.isValid()

        if not self.enabled:
            Logger.logWarning("[UrbanismValidator] Invalid urbanism raster file provided")
        
        return self.enabled

    def getClassGroup(self, raster_value: int) -> int:
        """Get class group for a raster value. Returns 0 if invalid/water."""
        if raster_value == self.WATER_CLASS:
            return 0  # Water body - invalid
        elif raster_value in self.GROUP_1_CLASSES:
            return 1  # Urban group
        elif raster_value in self.GROUP_2_CLASSES:
            return 2  # Rural group
        else:
            return 99  # Unknown class - treat as invalid

    def sampleRasterAtPoint(self, point_geom: QgsGeometry) -> int:
        """Sample raster value at given point geometry"""
        # TODO: Cache sample result of original centroids for performance (add new param original=True/False?)

        if not self.rasterLayer or not self.enabled:
            return -1
    
        point = point_geom.asPoint()

        # Reproject WGS84 → raster CRS
        src_crs = QgsCoordinateReferenceSystem("EPSG:4326")
        dest_crs = self.rasterLayer.crs()
        transform = QgsCoordinateTransform(src_crs, dest_crs, QgsProject.instance())
        point_in_raster_crs = transform.transform(point)
        # print(f"Sampling raster at point (raster CRS): {point_in_raster_crs.x()}, {point_in_raster_crs.y()}")

        sample_result = self.rasterLayer.dataProvider().sample(point_in_raster_crs, band=1)
    
        if sample_result[1]:  # Valid sample
            # print(f"Sampled raster result: {str(sample_result)}")
            return int(sample_result[0])
        else:
            return -1  # No data or outside raster extent

    def validateDisplacement(self, original_point: QgsGeometry, displaced_point: QgsGeometry) -> typing.Tuple[bool, str]:
        """
        Validate that displaced point is in compatible class group
        Returns (is_valid, error_message)
        """
        if not self.enabled:
            return True, ""
    
        # Get original point classification
        original_class = self.sampleRasterAtPoint(original_point)
        original_group = self.getClassGroup(original_class)
    
        # Check if original point is in water or invalid
        if original_group in [0, 99]:  # Water or invalid class
            error_msg = Errors.ErrorDisplayString.get(
                Errors.ErrorCode.ERROR_DISPLACER_ORIGINAL_POINT_IN_NOT_VALID_CLASS,
                "Original centroid is in non valid area"
            )
            #Logger.logWarning(f"[UrbanismValidator] Original centroid at water/invalid class {original_class}")
            return False, error_msg
    
        # Get displaced point classification
        displaced_class = self.sampleRasterAtPoint(displaced_point)
        displaced_group = self.getClassGroup(displaced_class)

        # print(f"Original class: {original_class} --> group: {original_group}")
        # print(f"Displaced class: {displaced_class} --> group: {displaced_group}")
        # print(f"Original: {original_class}, {original_group} --> Displaced: {displaced_class}, {displaced_group}")
    
        # Check if displaced point is in same group and not water
        if (displaced_group != original_group) or (displaced_group in [0, 99]):
            print("[UrbanismValidator] Displacement validation FAILED")
            error_msg = Errors.ErrorDisplayString.get(
                Errors.ErrorCode.ERROR_DISPLACER_URBANISM_CONSTRAINT_VIOLATED,
                "Displaced point violates urbanism class group constraint"
            )
            return False, error_msg
    
        # print("[UrbanismValidator] Displacement validated successfully")
        return True, ""

    # def getValidationRemark(self, original_point: QgsGeometry, displaced_point: QgsGeometry) -> str:
    #     """Get validation remark for output layer"""
    #     if not self.enabled:
    #         return ""
    
    #     is_valid, error_msg = self.validateDisplacement(original_point, displaced_point)
    #     return error_msg if not is_valid else ""