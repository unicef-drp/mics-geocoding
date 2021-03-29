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

from pathlib import Path

import typing
from enum import Enum
from .Logger import Logger

class LayersName(str, Enum):
    """ Layer - handle layer naming
    """
    CENTROIDS = "Cluster Centroids"
    POLYGONS = "Cluster Polygons"
    GPS = "GPS Cluster Points"
    MULTIPLT = "Cluster Multi-Points"  # Utils.LayersName.MULTIPLT
    CONVEXHULL = "Cluster Convex Hulls"  # Utils.LayersName.CONVEXHULL

    BUFFERS = "Cluster Buffers"  # Utils.LayersName.BUFFERS
    # Utils.LayersName.BUFFERSANON
    BUFFERSANON = "Cluster Anonymized Buffers"
    LINKS = "Cluster Displacement Links"  # Utils.LayersName.LINKS

    DISPLACED = "Cluster Displaced Centroids"  # Utils.LayersName.DISPLACED
    # cluster_anonym_disp_centroid
    DISPLACEDANON = "Cluster Anonymized Displaced Centroids"
    # create layer for displaced centroids

def removeLayerIfExists(layerName: str) -> None:
    """ Remove existing layer with the same name. Avoid duplication when run multiple times.
    """
    layers = QgsProject.instance().mapLayersByName(layerName)
    if layers:
        QgsProject.instance().removeMapLayer(layers[0])

def putLayerOnTopIfExists(layerName: str) -> None:
    """ Put layer on top if it exists
    """
    layers = QgsProject.instance().mapLayersByName(layerName)
    if layers:
        lyr = QgsProject.instance().takeMapLayer(layers[0])
        if lyr:
            QgsProject.instance().addMapLayer(lyr)


def createLayer(layerType: str, layerName: str, layerAttributes: typing.List[QgsField]) -> QgsVectorLayer:
    """ Create layer method, given a type, a name and some attributes
    """
    removeLayerIfExists(layerName)

    layer = QgsVectorLayer(layerType, layerName, 'memory')
    provider = layer.dataProvider()
    provider.addAttributes(layerAttributes)
    layer.updateFields()
    return layer


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
        Logger.logInfo("[MANAGER] CSV type")
        with open(file, "r") as f:
            fieldList = f.readline().strip().split(',')
    return fieldList

def layerCrossesTheMeridian(layer) -> bool:
    try:
        ext = layer.extent()
        return ext.xMinimum() == -180 and ext.xMaximum() == 180
    except:
        return False
