## ###########################################################################
##
# CentroidBuffersMaxDistanceComputer.py
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

from . import CentroidsLoader as CentroidsLoader
from . import ReferenceLayer as ReferenceLayer
from . import Utils
from .Transforms import Transforms
from .Logger import Logger

## #############################################################
# Centroids Displacer
## #############################################################


class CentroidBuffersMaxDistanceComputer():
    """ Handle the centroids buffer radiuses computation
        The radiuses are available through a dict: { cluster_id -> radius }
    """

    def __init__(self):
        self.maxDistance = {}
        self.__rural_displaced_points_count = 0
        self.__radius10000_indexes = []
        self.centroidLayer = None

    def computeBufferRadiusesCentroids(self) -> typing.NoReturn:
        """ Facade method that handle all the centroids buffer radiuses computation
        """
        self.maxDistance = {}
        self.__rural_displaced_points_count = 0
        self.__radius10000_indexes = []

        if self.centroidLayer:
            # Comput rural indexes for 10000 radius
            count_rural = sum(cluster_centroid_ft[1] == Utils.FieldAreaType.RURAL for cluster_centroid_ft in self.centroidLayer.getFeatures())
            if count_rural > 0:
                count_radius10000 = max(int(round(count_rural // 100)), 1)  # at least one
                self.__radius10000_indexes = random.sample(range(0, count_rural), count_radius10000)

            # Compute radiuses foreach points
            for cluster_centroid_ft in self.centroidLayer.getFeatures():
                # self.__displaceCentroid(cluster_centroid_ft)

                # define max distance depending on cluster type
                cluster_id = cluster_centroid_ft[0]
                cluster_type = cluster_centroid_ft[1]

                max_displace_distance = 0

                if cluster_type == Utils.FieldAreaType.URBAN:
                    max_displace_distance = 2000
                elif cluster_type == Utils.FieldAreaType.RURAL:
                    if self.__rural_displaced_points_count in self.__radius10000_indexes:  # Generate one int between 1 and 100, and test if it's equal to a specific value. equivalent to 1 % of chances.
                        max_displace_distance = 10000
                    else:
                        max_displace_distance = 5000
                        # Logger.logInfo("[------] compute " + str(cluster_id) + " = " + str(max_displace_distance) + " [type is" + cluster_type + "]")
                    self.__rural_displaced_points_count += 1
                else:
                    max_displace_distance = 5000

                self.maxDistance[cluster_id] = max_displace_distance
