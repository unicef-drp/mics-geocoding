## ###########################################################################
##
# CentroidsDisplacer.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

import math
import random
import typing

from qgis.core import *  # QGIS3
from qgis.PyQt.QtCore import QVariant
from datetime import datetime

from . import Utils

from .Transforms import Transforms
from .Logger import Logger

## #############################################################
# Centroids Displacer
## #############################################################


class CentroidBuffersLayerWriter():
    """ Facade that handle the writing of centroid buffers layer.
    """

    def __init__(self):
        self.__generatedLayers = {}  # layer collection for centroids dispalcement

        self.maxDistances = None

    def writerCentroidBuffersLayer(self) -> typing.NoReturn:
        """ Facade method that creates the new buffer, and gather the different field values
        """
        Logger.logInfo("[CentroidBuffersLayerWriter] Centroids displacement starts at {}".format(datetime.now()))

        self.clearLayers()

        if not self.maxDistances:
            return

        centroidLayer = Utils.getLayerIfExists(Utils.LayersType.CENTROIDS)

        # create layer for anonymised buffers
        self.__generatedLayers[Utils.LayersType.CENTROIDS_BUFFERS] = Utils.createLayer('Polygon?crs='+Transforms.layer_proj, Utils.LayersType.CENTROIDS_BUFFERS, [
            QgsField("cluster", QVariant.Int),
            QgsField("buf_dist", QVariant.Int)
        ])

        # Displace points
        for centroid_ft in centroidLayer.getFeatures():
            id = centroid_ft['cluster']
            dist = self.maxDistances[id]

            buffer_geom_tmp = QgsGeometry(centroid_ft.geometry())        # transform copy of the centroid into Web Mercator
            buffer_geom_tmp.transform(Transforms.tr)

            # create buffers around centroids
            buffer_geom = buffer_geom_tmp.buffer(dist, 20)

            buffer_geom.transform(Transforms.tr_back)

            centroid_buffer_ft = QgsFeature()
            centroid_buffer_ft.setGeometry(buffer_geom)
            centroid_buffer_ft.setAttributes([
                id,
                dist
            ])

            self.__generatedLayers[Utils.LayersType.CENTROIDS_BUFFERS].dataProvider().addFeatures([centroid_buffer_ft])

        QgsProject.instance().addMapLayer(self.__generatedLayers[Utils.LayersType.CENTROIDS_BUFFERS])

        Utils.writeLayerIfExists(Utils.LayersType.CENTROIDS_BUFFERS)
        Utils.putLayerOnTopIfExists(Utils.LayersType.DISPLACEDANON)  # fix z order
        Utils.putLayerOnTopIfExists(Utils.LayersType.DISPLACED)  # fix z order
        Utils.putLayerOnTopIfExists(Utils.LayersType.LINKS)  # fix z order
        Utils.putLayerOnTopIfExists(Utils.LayersType.CENTROIDS)  # fix z order

        Utils.reloadLayerFromDiskToAvoidMemoryFlag(Utils.LayersType.CENTROIDS_BUFFERS)

        Logger.logInfo("[CentroidBuffersLayerWriter] Centroids displacement finished at {}".format(datetime.now()))

    def clearLayers(self) -> typing.NoReturn:
        """ Clear all the layers of project instance that have been generated by this class
        """
        Utils.removeLayerIfExists(Utils.LayersType.CENTROIDS_BUFFERS)

        self.__generatedLayers.clear()
