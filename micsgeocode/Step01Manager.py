## ###########################################################################
##
# Step01Manager.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

import typing
from qgis.core import *  # QGIS3
from qgis.PyQt.QtCore import QVariant

from . import CentroidsLoader as CentroidsLoader
from . import CentroidsDisplacer as CentroidsDisplacer

from . import Utils
from .Logger import Logger
from datetime import datetime

####################################################################
# Class Step01Manager
####################################################################

class Step01Manager():
    """ Facade that handle step 1 of the algo.
        set inputs, call loader and displacef with proper arguments.
    """

    def __init__(self):
        self.layers = {}
        self.centroidLoader = CentroidsLoader.CentroidsLoader()
        self.centroidDisplacer = CentroidsDisplacer.CentroidsDisplacer()

####################################################################
# Main steps.
####################################################################

    def loadCentroids(self) -> None:
        self.centroidDisplacer.clearLayers()
        self.layers[Utils.LayersName.CENTROIDS] = self.centroidLoader.loadCentroids()
        Logger.logInfo("load centroids manager: " + str(hex(id(self.layers[Utils.LayersName.CENTROIDS]))))

    def displaceCentroids(self) -> None:
        Logger.logInfo("[MANAGER] Begin to displace the centroids at {}".format(datetime.now()))
        self.centroidLoader.putLayersOnTop()
        layers = QgsProject.instance().mapLayersByName(Utils.LayersName.CENTROIDS)
        if not layers:
            self.loadCentroids()
        self.centroidDisplacer.setCentroidsLayer(self.layers[Utils.LayersName.CENTROIDS])
        self.centroidDisplacer.displaceCentroids()

        Logger.logInfo("[MANAGER] Centroids displaced at {}".format(datetime.now()))

####################################################################
# accessors
####################################################################

    def setLatField(self, field: str) -> None:
        self.centroidLoader.lat_field = 'Lat'

    def setLongField(self, field: str) -> None:
        self.centroidLoader.lon_field = field

    def setClusterNoField(self, field: str) -> None:
        self.centroidLoader.cluster_no_field = field
        self.centroidDisplacer.cluster_no_field = field

    def setClusterTypeField(self, field: str) -> None:
        self.centroidLoader.cluster_type_field = field
        self.centroidDisplacer.cluster_type_field = field

    def setCentroidFile(self, file: str) -> None:
        self.centroidLoader.input_file = file

    def setReferenceLayer(self, ref_lyr_file: str) -> None:
        # load reference layer
        self.centroidDisplacer.setReferenceLayer(ref_lyr_file)
        self.centroidLoader.putLayersOnTop()

    def setReferenceLayerField(self, ref_id_field: str) -> None:
        self.centroidDisplacer.ref_id_field = ref_id_field

    def setUrbanTypes(self, types: typing.List[str]) -> None:
        self.centroidDisplacer.urban_types = types

    def setRuralTypes(self, types: typing.List[str]) -> None:
        self.centroidDisplacer.rural_types = types
