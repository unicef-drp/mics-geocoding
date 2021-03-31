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
from . import CentroidsLoader as CentroidsLoader
from . import CentroidsDisplacer as CentroidsDisplacer
from . import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3

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
        self.isLoaded = False
        self.isDisplaced = False

####################################################################
# Main steps.
####################################################################

    def loadCentroids(self) -> typing.NoReturn:
        self.centroidDisplacer.clearLayers()
        self.layers[Utils.LayersType.CENTROIDS] = self.centroidLoader.loadCentroids()
        self.isLoaded = True

    def displaceCentroids(self) -> typing.NoReturn:
        self.centroidLoader.putLayersOnTop()
        self.centroidDisplacer.setCentroidsLayer(self.layers[Utils.LayersType.CENTROIDS])
        self.centroidDisplacer.displaceCentroids()
        self.isDisplaced = True

####################################################################
# accessors
####################################################################

    def clusterAnonymizedBuffers(self) -> typing.Tuple[QgsVectorLayer, str, str]:
        layer = None
        layers = QgsProject.instance().mapLayersByName(Utils.LayersName.layerName(Utils.LayersType.BUFFERSANON))
        if layers:
            layer = layers[0]
        return layer, 'cluster', Utils.LayersName.fileName(Utils.LayersType.BUFFERSANON)

####################################################################
# accessors
####################################################################

    def setBasename(self, basename: str) -> typing.NoReturn:
        self.centroidLoader.clearLayers()
        self.centroidDisplacer.clearLayers()
        Utils.LayersName.basename = basename
        if self.isLoaded:
            self.loadCentroids()
        if self.isDisplaced:
            self.displaceCentroids()

    def setCentroidFile(self, file: str) -> typing.NoReturn:
        self.centroidLoader.input_file = file

    def setClusterNoField(self, field: str) -> typing.NoReturn:
        self.centroidLoader.cluster_no_field = field
        self.centroidDisplacer.cluster_no_field = field

    def setClusterTypeField(self, field: str) -> typing.NoReturn:
        self.centroidLoader.cluster_type_field = field
        self.centroidDisplacer.cluster_type_field = field

    def setLatField(self, field: str) -> typing.NoReturn:
        self.centroidLoader.lat_field = 'Lat'

    def setLongField(self, field: str) -> typing.NoReturn:
        self.centroidLoader.lon_field = field

    def setOutputsDirectory(self, dir: str) -> typing.NoReturn:
        Utils.LayersName.outputDirectory = dir

    def setReferenceLayer(self, ref_lyr_file: str) -> typing.NoReturn:
        self.centroidDisplacer.setReferenceLayer(ref_lyr_file)
        self.centroidLoader.putLayersOnTop()

    def setReferenceLayerField(self, ref_id_field: str) -> typing.NoReturn:
        self.centroidDisplacer.ref_id_field = ref_id_field

    def setRuralTypes(self, types: typing.List[str]) -> typing.NoReturn:
        self.centroidDisplacer.rural_types = types

    def setUrbanTypes(self, types: typing.List[str]) -> typing.NoReturn:
        self.centroidDisplacer.urban_types = types

