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


# ToDo: for buffers crossing antimeridian, use a modified CS: "GEOGCRS["WGS 84",
#     DATUM["World Geodetic System 1984",
#         ELLIPSOID["WGS 84",6378137,298.257223563,
#             LENGTHUNIT["metre",1]]],
#     PRIMEM["Greenwich",180,
#         ANGLEUNIT["degree",0.0174532925199433]],
#     CS[ellipsoidal,2],
#         AXIS["geodetic latitude (Lat)",north,
#             ORDER[1],
#             ANGLEUNIT["degree",0.0174532925199433]],
#         AXIS["geodetic longitude (Lon)",east,
#             ORDER[2],
#             ANGLEUNIT["degree",0.0174532925199433]],
#     USAGE[
#         SCOPE["unknown"],
#         AREA["World"],
#         BBOX[-90,-180,90,180]]]"

import math
import random

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


class CentroidsDisplacer():
    """ Handle the centroids displacement.
        The existing centroids are available through a map layer.
    """

    def __init__(self):
        self.urban_types = []  # values form the cluster type column that belong to urban type
        self.rural_types = []  # values form the cluster type column that belong to rural type
        self.__generatedLayers = {}  # layer collection for centroids dispalcement
        self.__rural_displaced_points = 0
        self.ref_id_field = ""
        self.referenceLayer = ReferenceLayer.ReferenceLayer()
        self.centroidLayer = None

    def displaceCentroids(self):
        """ Facade method that handle all the centroids displacement.
        """
        self.clearLayers()
        self.__rural_displaced_points = 0

        Logger.logInfo("Begin to displace the centroids at {}".format(datetime.now()))

        self.__createOutputsMemoryLayer()

        # Displace points
        for cluster_centroid_ft in self.centroidLayer.getFeatures():
            self.__displaceCentroid(cluster_centroid_ft)

        self.writeLayers()

        Logger.logSuccess("Centroids succcessfully displaced at {}".format(datetime.now()))

    def clearLayers(self) -> None:
        Utils.removeLayerIfExists(Utils.LayersType.BUFFERS)
        Utils.removeLayerIfExists(Utils.LayersType.BUFFERSANON)
        Utils.removeLayerIfExists(Utils.LayersType.LINKS)
        Utils.removeLayerIfExists(Utils.LayersType.DISPLACED)
        Utils.removeLayerIfExists(Utils.LayersType.DISPLACEDANON)
        self.__generatedLayers.clear()

    def setReferenceLayer(self, referenceLayer):
        self.clearLayers()
        self.referenceLayer.load(referenceLayer)

    def setCentroidsLayer(self, centroidsLayer):
        self.centroidLayer = centroidsLayer

    def writeLayers(self) -> None:
        Utils.writeLayerIfExists(Utils.LayersType.BUFFERS)
        Utils.writeLayerIfExists(Utils.LayersType.BUFFERSANON)
        Utils.writeLayerIfExists(Utils.LayersType.LINKS)
        Utils.writeLayerIfExists(Utils.LayersType.DISPLACED)
        Utils.writeLayerIfExists(Utils.LayersType.DISPLACEDANON)

####################################################################
# DisplaceCentroids
####################################################################

    def __displaceCentroid(self, cluster_centroid_ft):
        # copy geometry of centroid
        cluster_centroid_ft_geom_merc = QgsGeometry(cluster_centroid_ft.geometry())
        # transform copy of the centroid into Web Mercator
        cluster_centroid_ft_geom_merc.transform(Transforms.tr)
        # cluster_centroid_ft_geom_merc

        # cluster centroid coordinates in Web Mercator
        x = cluster_centroid_ft_geom_merc.asPoint().x()
        y = cluster_centroid_ft_geom_merc.asPoint().y()

        # get subnational ID for the cluster
        subnational_ids = self.referenceLayer.ref_fts_index.intersects(cluster_centroid_ft.geometry().boundingBox())
        intersecting_fts = []
        for s in subnational_ids:
            ft = self.referenceLayer.layer.getFeature(s)
            if ft.geometry().intersects(cluster_centroid_ft.geometry()):
                intersecting_fts.append(ft)
        if len(intersecting_fts) == 0:
            ref_id_before = 'None'
        elif len(intersecting_fts) == 1:
            ref_ft_before = intersecting_fts[0]
            ref_id_before = Utils.getval(ref_ft_before, self.ref_id_field)
        else:
            ref_id_before = 'Many'

        cluster_type = cluster_centroid_ft[1]
        # define max distance depending on cluster type
        if cluster_type in self.urban_types:
            max_displace_distance = 2000
        elif cluster_type in self.rural_types:
            self.__rural_displaced_points += 1
            max_displace_distance = (self.__rural_displaced_points % 100 == 0) and 10000 or 5000
        else:
            max_displace_distance = 5000

        # iterate
        con = True
        iterations = 0
        while con:
            # call displacement function
            new_x, new_y, distance, angle_degree = self.__displacepoint(x, y, max_displace_distance)

            # create geometry of a displaced centroid in Web Mercator
            displaced_point_mercator = QgsPointXY(new_x, new_y)

            # copy geometry of a displaced centroid
            displaced_point_wgs = QgsGeometry.fromPointXY(displaced_point_mercator)

            # transform copy of geometry of a displaced centroid into WGS84
            displaced_point_wgs.transform(Transforms.tr_back)
            # displaced_point_wgs

            # get subnational ID for the cluster
            subnational_ids_after = self.referenceLayer.ref_fts_index.intersects(displaced_point_wgs.boundingBox())
            intersecting_fts_after = []
            for s in subnational_ids_after:
                ft = self.referenceLayer.layer.getFeature(s)
                if ft.geometry().intersects(displaced_point_wgs):
                    intersecting_fts_after.append(ft)
            if len(intersecting_fts_after) == 0:
                ref_id_after = 'None'
            elif len(intersecting_fts_after) == 1:
                ref_ft_after = intersecting_fts_after[0]
                ref_id_after = Utils.getval(ref_ft_after, self.ref_id_field)
            else:
                ref_id_after = 'Many'

            if ref_id_after == ref_id_before:
                con = False
            iterations += 1
            Logger.logInfo("Cluster: {}, ref_id_before: {}, ref_id_after: {}, iteration: {}". format(cluster_centroid_ft['cluster'], ref_id_before, ref_id_after, iterations))
            if iterations > 10:
                con = False

        self.__updateOutputsMemoryLayer(
            cluster_centroid_ft,
            displaced_point_wgs,
            distance,
            angle_degree,
            ref_id_before,
            max_displace_distance,
            ref_id_after,
            iterations)

####################################################################
# DisplacePoint
####################################################################

    def __displacepoint(self, x, y, max_distance=5000):
        # calculates new point up to a given distance away from original point.All values should be provided in meters

        # Generate a random angle between 0 and 360
        angle_degree_internal = random.randint(0, 360)
        # Convert the random angle from degrees to radians
        angle_radian = angle_degree_internal * (math.pi / 180)

        # Generate a random distance by multiplying the max distance by a random number between 0 and 1
        distance_internal = random.random() * max_distance

        # Generate the offset by applying trig formulas (law of cosines) using the distance as the hypotenuse solving for
        # the other sides
        x_offset = math.sin(angle_radian) * distance_internal
        y_offset = math.cos(angle_radian) * distance_internal
        if 90 < angle_degree_internal <= 270:
            x_offset *= -1
        if angle_degree_internal > 180:
            y_offset *= -1

        # Add the offset to the original coordinate (in meters)
        new_x_internal = x + x_offset
        new_y_internal = y + y_offset

        return new_x_internal, new_y_internal, distance_internal, angle_degree_internal

####################################################################
# Layers
####################################################################

    def __createOutputsMemoryLayer(self):
        # create layer for buffers
        self.__generatedLayers[Utils.LayersType.BUFFERS] = Utils.createLayer('Polygon?crs='+Transforms.layer_proj, Utils.LayersType.BUFFERS, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("buf_dist", QVariant.Double)])

        # create layer for anonymized buffers
        self.__generatedLayers[Utils.LayersType.BUFFERSANON] = Utils.createLayer('Polygon?crs='+Transforms.layer_proj, Utils.LayersType.BUFFERSANON, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("buf_dist", QVariant.Double)])

        # create layer for displacement links
        self.__generatedLayers[Utils.LayersType.LINKS] = Utils.createLayer('LineString?crs='+Transforms.layer_proj, Utils.LayersType.LINKS, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("lon_orig", QVariant.Double), QgsField("lat_orig", QVariant.Double), QgsField("lon_disp", QVariant.Double), QgsField("lat_disp", QVariant.Double), QgsField("disp_dist_m", QVariant.Double), QgsField("disp_angle", QVariant.Double), QgsField("refar_id_b", QVariant.String), QgsField("refar_id_a", QVariant.String), QgsField("iter", QVariant.Int)])

        # create layer for displaced centroids
        self.__generatedLayers[Utils.LayersType.DISPLACED] = Utils.createLayer('Point?crs='+Transforms.layer_proj, Utils.LayersType.DISPLACED, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("lon_orig", QVariant.Double), QgsField("lat_orig", QVariant.Double), QgsField("lon_disp", QVariant.Double), QgsField("lat_disp", QVariant.Double), QgsField("disp_dist_m", QVariant.Double), QgsField("disp_angle", QVariant.Double), QgsField("refar_id_b", QVariant.String), QgsField("refar_id_a", QVariant.String), QgsField("iter", QVariant.Int)])

        # create layer for anonymized displaced centroids
        self.__generatedLayers[Utils.LayersType.DISPLACEDANON] = Utils.createLayer('Point?crs='+Transforms.layer_proj, Utils.LayersType.DISPLACEDANON, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("lon_disp", QVariant.Double), QgsField("lat_disp", QVariant.Double)])

        # add layers to project following correct z order
        QgsProject.instance().addMapLayer(self.__generatedLayers[Utils.LayersType.BUFFERS])
        QgsProject.instance().addMapLayer(self.__generatedLayers[Utils.LayersType.BUFFERSANON])
        QgsProject.instance().addMapLayer(self.__generatedLayers[Utils.LayersType.LINKS])
        Utils.putLayerOnTopIfExists(Utils.LayersType.CENTROIDS) # fix z order
        QgsProject.instance().addMapLayer(self.__generatedLayers[Utils.LayersType.DISPLACED])
        QgsProject.instance().addMapLayer(self.__generatedLayers[Utils.LayersType.DISPLACEDANON])

    def __updateOutputsMemoryLayer(self, cluster_centroid_ft, displaced_point_wgs, distance, angle_degree, ref_id_before, max_displace_distance, ref_id_after, iterations):
        # add displaced centroid
        feat_disp_centroid = QgsFeature()
        feat_disp_centroid.setGeometry(displaced_point_wgs)
        feat_disp_centroid.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], cluster_centroid_ft['count'], cluster_centroid_ft.geometry().asPoint().x(), cluster_centroid_ft.geometry().asPoint().y(), displaced_point_wgs.asPoint().x(), displaced_point_wgs.asPoint().y(), distance, angle_degree, ref_id_before, ref_id_after, iterations])
        self.__generatedLayers[Utils.LayersType.DISPLACED].dataProvider().addFeatures([feat_disp_centroid])

        # add anoymized displaced centroid
        feat_anonym_disp_centroid = QgsFeature()
        feat_anonym_disp_centroid.setGeometry(displaced_point_wgs)
        feat_anonym_disp_centroid.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], displaced_point_wgs.asPoint().x(), displaced_point_wgs.asPoint().y()])
        self.__generatedLayers[Utils.LayersType.DISPLACEDANON].dataProvider().addFeatures([feat_anonym_disp_centroid])

        # add displacement links
        centroid_disp_links_ft = QgsFeature()
        centroid_disp_links_ft.setGeometry(QgsGeometry.fromPolylineXY([cluster_centroid_ft.geometry().asPoint(), feat_disp_centroid.geometry().asPoint()]))
        centroid_disp_links_ft.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], cluster_centroid_ft['count'], cluster_centroid_ft.geometry().asPoint().x(), cluster_centroid_ft.geometry().asPoint().y(), displaced_point_wgs.asPoint().x(), displaced_point_wgs.asPoint().y(), distance, angle_degree, ref_id_before, ref_id_after, iterations])
        self.__generatedLayers[Utils.LayersType.LINKS].dataProvider().addFeatures([centroid_disp_links_ft])

        # copy geometry of displaced centroid
        displaced_feat_centroid_mercator = QgsGeometry(feat_disp_centroid.geometry())

        # transform copy of the centroid into Web Mercator
        displaced_feat_centroid_mercator.transform(Transforms.tr)
        # create buffers around displaced centroids
        disp_centroid_buff_geom = displaced_feat_centroid_mercator.buffer(max_displace_distance, 20)

        disp_centroid_buff_geom.transform(Transforms.tr_back)
        disp_centroid_buff_ft = QgsFeature()
        disp_centroid_buff_ft.setGeometry(disp_centroid_buff_geom)
        disp_centroid_buff_ft.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], cluster_centroid_ft['count'], max_displace_distance])
        self.__generatedLayers[Utils.LayersType.BUFFERS].dataProvider().addFeatures([disp_centroid_buff_ft])

        # create buffers around displaced centroids
        disp_anonym_centroid_buff_ft = QgsFeature()
        disp_anonym_centroid_buff_ft.setGeometry(disp_centroid_buff_geom)
        disp_anonym_centroid_buff_ft.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], max_displace_distance])
        self.__generatedLayers[Utils.LayersType.BUFFERSANON].dataProvider().addFeatures([disp_anonym_centroid_buff_ft])

        # create buffers around original centroids
        # centroid_buff = cluster_centroid_ft_geom_merc.buffer(max_displace_distance, 20)
        # centroid_buff.transform(Transforms.tr_back)
        # feat_centroid_buff = QgsFeature()
        # feat_centroid_buff.setGeometry(centroid_buff)
        # feat_centroid_buff.setAttributes([cl[0], cl[1], counter, max_displace_distance])
        # Utils.LayersType.BUFFERS_prov.addFeatures([feat_centroid_buff])
