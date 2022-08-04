## ###########################################################################
##
# Utils.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

from qgis.core import *  # QGIS3

from PyQt5 import QtCore

from pathlib import Path

import typing
from enum import Enum
from .Logger import Logger


class LayersType(str, Enum):
    CENTROIDS = "CENTROIDS"
    POLYGONS = "POLYGONS"
    GPS = "GPS"
    MULTIPLT = "MULTIPLT"
    CONVEXHULL = "CONVEXHULL"
    BUFFERS = "BUFFERS"
    BUFFERSANON = "BUFFERSANON"
    LINKS = "LINKS"
    DISPLACED = "DISPLACED"
    DISPLACEDANON = "DISPLACEDANON"


class LayersName():
    basename = ""
    outputDirectory = ""
    layerNames = {
        LayersType.CENTROIDS: "cluster_centroids",
        LayersType.POLYGONS: "cluster_polygons",
        LayersType.GPS: "cluster_points",
        LayersType.MULTIPLT: "cluster_multi-points",
        LayersType.CONVEXHULL: "cluster_convex_hulls",
        LayersType.BUFFERSANON: "cluster_anonymised_buffers",
        LayersType.LINKS: "cluster_displacement_links",
        LayersType.DISPLACED: "cluster_unanonymised_displaced_centroids",
        LayersType.DISPLACEDANON: "cluster_anonymised_displaced_centroids",
    }

    @staticmethod
    def layerName(t: LayersType) -> str:
        """ generates layer name for UI
        """
        if LayersName.basename:
            return LayersName.basename + '_' + LayersName.layerNames[t]
        return LayersName.layerNames[t]

    @staticmethod
    def fileName(t: LayersType) -> str:
        """ generates layer name for file
        """
        if LayersName.basename:
            return LayersName.outputDirectory + QtCore.QDir.separator() + LayersName.basename + '_' + LayersName.layerNames[t] + ".shp"
        return LayersName.outputDirectory + QtCore.QDir.separator() + LayersName.layerNames[t] + ".shp"

    @staticmethod
    def customfileName(base: str) -> str:
        """ generates layer name for file
        """
        if LayersName.basename:
            return LayersName.outputDirectory + QtCore.QDir.separator() + LayersName.basename + '_' + base + ".shp"
        return LayersName.outputDirectory + QtCore.QDir.separator() + base + ".shp"


def removeLayerIfExistsByName(layerName: str) -> typing.NoReturn:
    """ Remove existing layer with the same name. Avoid duplication when run multiple times.
    """
    layers = QgsProject.instance().mapLayersByName(layerName)
    if layers:
        QgsProject.instance().removeMapLayer(layers[0])


def removeLayerIfExists(layerType: LayersType) -> typing.NoReturn:
    """ Remove existing layer with the same name. Avoid duplication when run multiple times.
    """
    layers = QgsProject.instance().mapLayersByName(LayersName.layerName(layerType))
    if layers:
        QgsProject.instance().removeMapLayer(layers[0])


def putLayerOnTopIfExists(layerType: LayersType) -> typing.NoReturn:
    """ Put layer on top if it exists
    """
    layers = QgsProject.instance().mapLayersByName(LayersName.layerName(layerType))
    if layers:
        lyr = QgsProject.instance().takeMapLayer(layers[0])
        if lyr:
            QgsProject.instance().addMapLayer(lyr)


def createLayer(layerType: str, layerCategorie: LayersType, layerAttributes: typing.List[QgsField]) -> QgsVectorLayer:
    """ Create layer method, given a type, a name and some attributes
    """
    removeLayerIfExists(layerCategorie)

    # error = QgsVectorFileWriter.writeAsVectorFormatV2(layer, "testdata/my_new_shapefile", transform_context, save_options)
    layer = QgsVectorLayer(layerType, LayersName.layerName(layerCategorie), 'memory')
    layer.setCustomProperty("skipMemoryLayersCheck", 1)
    provider = layer.dataProvider()
    provider.addAttributes(layerAttributes)
    layer.updateFields()

    return layer


def reloadLayerFromDiskToAvoidMemoryFlag(layerType: LayersType) -> typing.NoReturn:
    """ Close the layer, if it exists. Then reopen it, from the file. To avoid the weird 'memory' flag
    """
    filename = LayersName.fileName(layerType)
    layerName = LayersName.layerName(layerType)

    removeLayerIfExists(layerType)

    layer = QgsVectorLayer(filename, layerName)
    QgsProject.instance().addMapLayer(layer)


def writeLayerIfExists(layerType: LayersType) -> typing.NoReturn:
    """ Write hte layer on disk, if it exists in the project instance
    """
    layers = QgsProject.instance().mapLayersByName(LayersName.layerName(layerType))
    if layers:
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "ESRI Shapefile"

        # writer = QgsVectorFileWriter( "output_path_and_name.shp", provider.encoding(), provider.fields(), QGis.WKBPolygon, provider.crs() )
        writer = QgsVectorFileWriter.writeAsVectorFormatV2(
            layers[0],
            LayersName.fileName(layerType),
            QgsCoordinateTransformContext(),
            options)
        # Don't know how to manage this.
        # reloadLayerFromDiskToAvoidMemoryFlag(layerType)


def getval(ft: QgsFeature, field: QgsField) -> str:
    """ get value as string from feature / field combo
    """
    if field:
        val = ft[field]
        if val:
            if isinstance(val, basestring):
                # ToDo: decode or encode???: val.encode('UTF-8').strip()
                result = "{}".format(val.encode(
                    'UTF-8').decode('UTF-8').strip())
            else:
                result = "{}".format(val)
        else:
            result = ""
    else:
        result = ""
    return result


def getFieldsListAsStrArray(file: str) -> typing.List[str]:
    """ analyze file and retrieve field list
    """
    fieldList = []
    extension = Path(file).suffix[1:]
    if extension == "shp":
        layer = QgsVectorLayer(file, "tmp", "ogr")
        if layer:
            fieldList = [f.name() for f in layer.fields()]
    elif extension == "csv":
        with open(file, "r") as f:
            fieldList = f.readline().strip().split(',')
    elif extension == "txt":
        with open(file, "r") as f:
            line = f.readline()
            fieldList = line.strip().split('\t')

    return fieldList


def layerCrossesTheMeridian(layer: QgsVectorLayer) -> bool:
    """ add a convenient method that checks if a layer crosses the antimeridian
    """
    try:
        ext = layer.extent()
        return ext.xMinimum() == -180 and ext.xMaximum() == 180
    except:
        return False
