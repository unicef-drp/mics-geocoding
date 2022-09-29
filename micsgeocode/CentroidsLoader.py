## ###########################################################################
##
# CentroidsLoader.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

import re
import typing
from datetime import datetime

from qgis.core import *  # QGIS3
from qgis.PyQt.QtCore import QVariant

from . import Utils
from pathlib import Path
from .Transforms import Transforms
from .Logger import Logger

from . import Errors

## ###########################################################################
# Centroids Loader
## ###########################################################################


class CentroidsLoader():
    """ Handle the loading of centroids.
        2 types of inputs:
        - CSV: those are gps coordinates. Centroids are computed given those.
        - SHP: those are centroids. Centroidsare just loaded.
        The centroids are written in a map layer.
    """

    def __init__(self):
        self.input_file = ""
        self.layers = {}
        self.lat_field = "default"
        self.lon_field = "default"
        self.cluster_no_field = "default"
        self.cluster_type_field = "default"
        self.admin_boundaries_field = "default"

    def loadCentroids(self) -> Errors.ErrorCode:
        """ Facade method that handle all the centroids loading
        """
        # check type of input file: extension must be csv or shp
        # from there, with deduct two differents scenarios.
        Logger.logInfo("[CentroidsLoader] Centroids loading starts at {}".format(datetime.now()))

        self.clearLayers()

        if not self.input_file:
            return Errors.ErrorCode.ERROR_MISSING_INPUT

        Logger.logInfo("[CentroidsLoader] Loading from file: " + self.input_file)

        self.__initLayer(Utils.LayersType.CENTROIDS)

        input_file_clusters_format = Path(self.input_file).suffix[1:]
        if input_file_clusters_format == "shp":
            self.__loadCentroidsFromSHP()
        elif input_file_clusters_format == "csv":
            self.__loadCentroidsFromCSV()
        QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.CENTROIDS])

        self.writeLayers()

        self.reloadLayerFromDiskToAvoidMemoryFlag()

        return Errors.ErrorCode.SUCCESS

    def clearLayers(self) -> typing.NoReturn:
        """ Clear all the layers of project instance that have been generated by this class
        """
        Utils.removeLayerIfExists(Utils.LayersType.CENTROIDS)
        Utils.removeLayerIfExists(Utils.LayersType.POLYGONS)
        Utils.removeLayerIfExists(Utils.LayersType.GPS)
        Utils.removeLayerIfExists(Utils.LayersType.MULTIPLT)
        Utils.removeLayerIfExists(Utils.LayersType.CONVEXHULL)

        self.layers.clear()

    def putLayersOnTop(self) -> typing.NoReturn:
        """ Convenient method that put all those layers on tpop, following a correct z orders
        """
        Utils.putLayerOnTopIfExists(Utils.LayersType.GPS)
        Utils.putLayerOnTopIfExists(Utils.LayersType.MULTIPLT)
        Utils.putLayerOnTopIfExists(Utils.LayersType.CONVEXHULL)
        Utils.putLayerOnTopIfExists(Utils.LayersType.POLYGONS)
        Utils.putLayerOnTopIfExists(Utils.LayersType.CENTROIDS)

    def writeLayers(self) -> typing.NoReturn:
        """ Write all the layers handle by this class to files
        """
        Utils.writeLayerIfExists(Utils.LayersType.CENTROIDS)

        Logger.logInfo("[CentroidsLoader] Layers written to disk")

    def reloadLayerFromDiskToAvoidMemoryFlag(self) -> typing.NoReturn:
        """ Write all the layers handle by this class to files
        """
        Utils.reloadLayerFromDiskToAvoidMemoryFlag(Utils.LayersType.CENTROIDS)
        Logger.logInfo("[CentroidsLoader] Layers written to disk")

## ###########################################################################
# init layers
## ###########################################################################

    def __initLayer(self, type: Utils.LayersType):
        """ Init all layers
        """
        if type == Utils.LayersType.GPS:
            self.layers[Utils.LayersType.GPS] = Utils.createLayer('Point?crs='+Transforms.layer_proj, Utils.LayersType.GPS, [
                QgsField("cluster", QVariant.Int),
                QgsField("type", QVariant.String),
                QgsField("lon", QVariant.Double),
                QgsField("lat", QVariant.Double)
            ])

        elif type == Utils.LayersType.MULTIPLT:
            self.layers[Utils.LayersType.MULTIPLT] = Utils.createLayer('MultiPoint?crs='+Transforms.layer_proj, Utils.LayersType.MULTIPLT, [
                QgsField("cluster", QVariant.Int),
                QgsField("type", QVariant.String),
                QgsField("count", QVariant.Int)
            ])

        elif type == Utils.LayersType.CONVEXHULL:
            self.layers[Utils.LayersType.CONVEXHULL] = Utils.createLayer('Polygon?crs='+Transforms.layer_proj, Utils.LayersType.CONVEXHULL, [
                QgsField("cluster", QVariant.Int),
                QgsField("type", QVariant.String),
                QgsField("count", QVariant.Int),
                QgsField("area_m2", QVariant.Double),
                QgsField("angle_deg", QVariant.Double),
                QgsField("width_m", QVariant.Double),
                QgsField("height_m", QVariant.Double)
            ])
        elif type == Utils.LayersType.CENTROIDS:
            self.layers[Utils.LayersType.CENTROIDS] = Utils.createLayer('Point?crs='+Transforms.layer_proj, Utils.LayersType.CENTROIDS, [
                QgsField("cluster", QVariant.Int),
                QgsField("type", QVariant.String),
                QgsField("count", QVariant.Int),
                QgsField("admin", QVariant.String)
            ])

## ###########################################################################
# SHP Inputs
## ###########################################################################

    def __loadCentroidsFromSHP(self) -> typing.NoReturn:
        """ Handle loading from shp
        """
        Logger.logInfo("[CentroidsLoader] Cluster Numero field: " + self.cluster_no_field)
        Logger.logInfo("[CentroidsLoader] Cluster Type field: " + self.cluster_type_field)
        Logger.logInfo("[CentroidsLoader] Admin Boundaries field: " + self.admin_boundaries_field)

        self.layers[Utils.LayersType.POLYGONS] = QgsVectorLayer(self.input_file, Utils.LayersName.layerName(Utils.LayersType.POLYGONS), "ogr")

        Logger.logInfo(str(self.layers[Utils.LayersType.POLYGONS].wkbType()))

        if self.layers[Utils.LayersType.POLYGONS].wkbType() == 1:  # QgsWkbTypes.Point:

            gps_coords = self.__layer2gps(self.layers[Utils.LayersType.POLYGONS])
            self.__loadCentroidsFromGPSCoords(gps_coords)
            self.layers[Utils.LayersType.POLYGONS] = None

        elif self.layers[Utils.LayersType.POLYGONS].wkbType() == 4:  # QgsWkbTypes.MultiPoints: # 4

            # reproduce the csv input mecanism, to share the same algo. not very optimized, but hey.
            self.__initLayer(Utils.LayersType.MULTIPLT)
            self.__initLayer(Utils.LayersType.CONVEXHULL)

            gps_coords = self.__layer2gps(self.layers[Utils.LayersType.POLYGONS])
            self.__computeCentroidsfromGPSCoords(gps_coords)
            QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.MULTIPLT])
            QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.CONVEXHULL])

        elif self.layers[Utils.LayersType.POLYGONS].wkbType() == 6:  # QgsWkbTypes.Polygon: # 6
            cluster_polygons = [ft for ft in self.layers[Utils.LayersType.POLYGONS].getFeatures()]
            for cluster_polygon in cluster_polygons:
                cluster_centroid_ft = QgsFeature()
                cluster_centroid_ft.setAttributes([
                    cluster_polygon[self.cluster_no_field],
                    cluster_polygon[self.cluster_type_field],
                    1,
                    cluster_polygon[self.admin_boundaries_field]
                ])
                cluster_centroid_ft.setGeometry(cluster_polygon.geometry().poleOfInaccessibility(100)[0])
                self.layers[Utils.LayersType.CENTROIDS].dataProvider().addFeatures([cluster_centroid_ft])
                # cluster_centroid_fts.append(cluster_centroid_ft)
            QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.POLYGONS])

    def __layer2gps(self, layer) -> typing.List:
        """ extract from a layer a gps_coord list
        """
        gps_coords = []
        for feature in layer.getFeatures():
            geom = feature.geometry()
            for part in geom.parts():  # loop through the parts of each multipoint feature
                for p in part.vertices():  # now "loop through" each vertex of each part (actually a loop isnt really needed but easier to implement, since each part always has exact one vertex)
                    gps_coords.append({
                        'cluster': feature[self.cluster_no_field],
                        'type': feature[self.cluster_type_field],
                        'lat': p.y(),
                        'lon': p.x(),
                        'admin': feature[self.admin_boundaries_field]
                    })
        return gps_coords

## ###########################################################################
# CSV Inputs
## ###########################################################################

    def __loadCentroidsFromCSV(self) -> typing.NoReturn:
        """ Handle loading from csv
        """
        Logger.logInfo("[CentroidsLoader] Cluster Numero field: " + self.cluster_no_field)
        Logger.logInfo("[CentroidsLoader] Cluster Type field: " + self.cluster_type_field)
        Logger.logInfo("[CentroidsLoader] Cluster Longitude field: " + self.lon_field)
        Logger.logInfo("[CentroidsLoader] Cluster Latitude field: " + self.lat_field)
        Logger.logInfo("[CentroidsLoader] Admin Boundaries field: " + self.admin_boundaries_field)

        gps_coords = self.__csv2gps()

        self.__loadCentroidsFromGPSCoords(gps_coords)

    def __csv2gps(self) -> typing.List:
        """ Extract from a csv a gps_coord list
        """
        gps_coords = []
        with open(self.input_file, "r", encoding='utf-8-sig') as f:
            c = 0
            # parse csv file
            for g in f:
                if c == 0:
                    line = re.split(',', g.strip())
                    cluster_no_id = line.index(self.cluster_no_field)
                    cluster_type_id = line.index(self.cluster_type_field)
                    lat_id = line.index(self.lat_field)
                    lon_id = line.index(self.lon_field)
                    admin_boundaries_id = line.index(self.admin_boundaries_field)
                if c != 0:
                    line = re.split(',', g.strip())
                    gps_coords.append({
                        'cluster': int(line[cluster_no_id]),
                        'type': line[cluster_type_id],
                        'lat': float(line[lat_id]),
                        'lon': float(line[lon_id]),
                        'admin': line[admin_boundaries_id]
                    })
                c = c + 1
        return gps_coords

## ###########################################################################
# both inputs
## ###########################################################################

    def __addGpsLayer(self, gps_coords: typing.List) -> typing.NoReturn:
        """ Add a gps layer absed on gps_coords list
        """
        # add gps points to a layer
        for gps in gps_coords:
            point = QgsPointXY(gps['lon'], gps['lat'])
            gps_coords_ft = QgsFeature()
            gps_coords_ft.setGeometry(QgsGeometry.fromPointXY(point))
            gps_coords_ft.setAttributes([
                gps['cluster'],
                gps['type'],
                gps['lon'],
                gps['lat']
            ])
            self.layers[Utils.LayersType.GPS].dataProvider().addFeatures([gps_coords_ft])

    def __loadCentroidsFromGPSCoords(self, gps_coords: typing.List) -> typing.NoReturn:
        """ Load centroids from gps coords
        """
        self.__initLayer(Utils.LayersType.MULTIPLT)
        self.__initLayer(Utils.LayersType.CONVEXHULL)
        self.__computeCentroidsfromGPSCoords(gps_coords)

        isMultiPoint = self.layers[Utils.LayersType.MULTIPLT].featureCount() > 0
        if isMultiPoint:
            self.__initLayer(Utils.LayersType.GPS)
            self.__addGpsLayer(gps_coords)
            QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.GPS])

            QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.MULTIPLT])
            QgsProject.instance().addMapLayer(self.layers[Utils.LayersType.CONVEXHULL])
        else:
            Utils.removeLayerIfExists(Utils.LayersType.MULTIPLT)
            self.layers[Utils.LayersType.MULTIPLT] = None
            Utils.removeLayerIfExists(Utils.LayersType.CONVEXHULL)
            self.layers[Utils.LayersType.CONVEXHULL] = None

    def __computeCentroidsfromGPSCoords(self, gps_coords: typing.List) -> typing.NoReturn:
        """ Compute centroids from gps coords
        """
        unique_clusters = set(val['cluster'] for val in gps_coords)
        unique_clusters_with_type = []
        for unique_cluster in unique_clusters:
            cluster_type = sorted([val['type'] for val in gps_coords if val['cluster'] == unique_cluster])[0]
            unique_clusters_with_type.append(tuple((unique_cluster, cluster_type)))

        for cl in unique_clusters_with_type:
            self.__computeCentroid(cl, [val for val in gps_coords if val['cluster'] == cl[0]])

    def __computeCentroid(self, cluster, gps_coords_per_cluster: typing.List) -> typing.NoReturn:
        cluster_centroid_ft = QgsFeature()

        if len(gps_coords_per_cluster) == 1:
            point = QgsPointXY(gps_coords_per_cluster[0]['lon'], gps_coords_per_cluster[0]['lat'])
            cluster_centroid_ft.setGeometry(QgsGeometry.fromPointXY(point))
            cluster_centroid_ft.setAttributes([cluster[0], cluster[1], 1, gps_coords_per_cluster[0]['admin']])
        else:
            # compute gps coords list
            cluster_multipt_ft, gps_coords_list = self.__computeMultiptFeature(cluster, gps_coords_per_cluster)
            # compute convexhull
            cluster_convexhull_ft = self.__computeConvexhullFeature(cluster, gps_coords_list)
            # compute centroid
            cluster_centroid_ft.setAttributes([cluster[0], cluster[1], len(gps_coords_list), gps_coords_per_cluster[0]['admin']])
            self.__computeCentroidGeometry(cluster_centroid_ft, cluster_multipt_ft, cluster_convexhull_ft)

        self.layers[Utils.LayersType.CENTROIDS].dataProvider().addFeatures([cluster_centroid_ft])

    def __computeMultiptFeature(self, cluster, gps_coords_per_cluster: typing.List) -> typing.Tuple[QgsFeature, typing.List]:
        """ Compute multi point feature from a set of gps coords
        """
        gps_coords_list = []
        for p in gps_coords_per_cluster:
            point = QgsPointXY(p['lon'], p['lat'])
            gps_coords_list.append(point)

        cluster_multipt_ft = QgsFeature()
        cluster_multipt_ft.setGeometry(QgsGeometry.fromMultiPointXY(gps_coords_list))
        cluster_multipt_ft.setAttributes([cluster[0], cluster[1], len(gps_coords_list)])
        self.layers[Utils.LayersType.MULTIPLT].dataProvider().addFeatures([cluster_multipt_ft])
        return cluster_multipt_ft, gps_coords_list

    def __computeConvexhullFeature(self, cluster, gps_coords_list: typing.List) -> QgsFeature:
        """ Compute convex hull from a set of gps coords
        """
        # compute convexhull
        cluster_convexhull_ft = QgsFeature()
        cluster_convexhull_ft.setGeometry(QgsGeometry.fromPolygonXY([gps_coords_list]).convexHull())

        # calculate convex hull geometry params
        cluster_convexhull_geom_merc = QgsGeometry(cluster_convexhull_ft.geometry())
        cluster_convexhull_geom_merc.transform(Transforms.tr)
        cluster_convexhull_mbb = cluster_convexhull_geom_merc.orientedMinimumBoundingBox()

        area_m2 = cluster_convexhull_mbb[1]
        angle_deg = cluster_convexhull_mbb[2]
        width_m = cluster_convexhull_mbb[3]
        height_m = cluster_convexhull_mbb[4]

        if area_m2 == 1.7976931348623157e+308:
            area_m2 = 0  # handling infinity values
        if angle_deg == 1.7976931348623157e+308:
            angle_deg = 0  # handling infinity values
        if width_m == 1.7976931348623157e+308:
            width_m = 0  # handling infinity values
        if height_m == 1.7976931348623157e+308:
            height_m = 0  # handling infinity values

        cluster_convexhull_ft.setAttributes([cluster[0], cluster[1], len(gps_coords_list), area_m2, angle_deg, width_m, height_m])
        self.layers[Utils.LayersType.CONVEXHULL].dataProvider().addFeatures([cluster_convexhull_ft])

        return cluster_convexhull_ft

    def __computeCentroidGeometry(self, cluster_centroid_ft: QgsFeature, cluster_multipt_ft: QgsFeature, cluster_convexhull_ft: QgsFeature) -> typing.NoReturn:
        """ Compute the centroid geometry for a given centroid feature, the multi point and the convexhull
        """
        # determine if pole of inaccessibility can be determined
        if cluster_convexhull_ft.geometry().poleOfInaccessibility(100)[0].isNull():
            cluster_centroid_ft.setGeometry(cluster_multipt_ft.geometry().centroid())
        else:
            cluster_centroid_ft.setGeometry(cluster_convexhull_ft.geometry().poleOfInaccessibility(100)[0])
