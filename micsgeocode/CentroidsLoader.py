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
from datetime import datetime

from qgis.core import *  # QGIS3
from qgis.PyQt.QtCore import QVariant

from . import Utils
from pathlib import Path
from .Transforms import Transforms
from .Logger import Logger

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

    def loadCentroids(self) -> QgsVectorLayer:
        # check type of input file: extension must be csv or shp
        # from there, with deduct two differents scenarios.

        self.clearLayers()

        Logger.logInfo("Begin to load the centroids at {}".format(datetime.now()))
        self.layers[Utils.LayersName.CENTROIDS] = Utils.createLayer('Point?crs='+Transforms.layer_proj, Utils.LayersName.CENTROIDS, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int)])
        input_file_clusters_format = Path(self.input_file).suffix[1:]
        if input_file_clusters_format == "shp":
            Logger.logInfo("Centroids read from shapefile")
            self.__loadCentroidsFromSHP()
        elif input_file_clusters_format == "csv":
            Logger.logInfo("Centroids computed from csv")
            self.__loadCentroidsFromCSV()

        QgsProject.instance().addMapLayer(self.layers[Utils.LayersName.CENTROIDS])

        Logger.logSuccess(
            "Centroids succcessfully loaded at {}".format(datetime.now()))

        return self.layers[Utils.LayersName.CENTROIDS]

    def clearLayers(self) -> None:
        Utils.removeLayerIfExists(Utils.LayersName.CENTROIDS)
        Utils.removeLayerIfExists(Utils.LayersName.POLYGONS)
        Utils.removeLayerIfExists(Utils.LayersName.GPS)
        Utils.removeLayerIfExists(Utils.LayersName.MULTIPLT)
        Utils.removeLayerIfExists(Utils.LayersName.CONVEXHULL)

        self.layers.clear()

    def putLayersOnTop(self) -> None:
        Utils.putLayerOnTopIfExists(Utils.LayersName.GPS)
        Utils.putLayerOnTopIfExists(Utils.LayersName.MULTIPLT)
        Utils.putLayerOnTopIfExists(Utils.LayersName.CONVEXHULL)
        Utils.putLayerOnTopIfExists(Utils.LayersName.POLYGONS)
        Utils.putLayerOnTopIfExists(Utils.LayersName.CENTROIDS)

## ###########################################################################
# SHP Inputs
## ###########################################################################

    def __loadCentroidsFromSHP(self):
        self.layers[Utils.LayersName.POLYGONS] = QgsVectorLayer(self.input_file, Utils.LayersName.POLYGONS, "ogr")

        if self.layers[Utils.LayersName.POLYGONS].wkbType() == 1: # QgsWkbTypes.Point:
            cluster_centroids = [ft for ft in self.layers[Utils.LayersName.POLYGONS].getFeatures()]
            for cluster_centroid in cluster_centroids:
                cluster_centroid_ft = QgsFeature()
                cluster_centroid_ft.setAttributes([cluster_centroid[self.cluster_no_field], cluster_centroid[self.cluster_type_field], 1])
                cluster_centroid_ft.setGeometry(cluster_centroid.geometry())
                self.layers[Utils.LayersName.CENTROIDS].dataProvider().addFeatures([
                    cluster_centroid_ft])

        elif self.layers[Utils.LayersName.POLYGONS].wkbType() == 6: #QgsWkbTypes.Polygon: # 6
            cluster_polygons = [ft for ft in self.layers[Utils.LayersName.POLYGONS].getFeatures()]
            for cluster_polygon in cluster_polygons:
                cluster_centroid_ft = QgsFeature()
                cluster_centroid_ft.setAttributes([cluster_polygon[self.cluster_no_field], cluster_polygon[self.cluster_type_field], 1])
                cluster_centroid_ft.setGeometry(cluster_polygon.geometry().poleOfInaccessibility(100)[0])
                self.layers[Utils.LayersName.CENTROIDS].dataProvider().addFeatures([cluster_centroid_ft])
                # cluster_centroid_fts.append(cluster_centroid_ft)

        QgsProject.instance().addMapLayer(self.layers[Utils.LayersName.POLYGONS])

## ###########################################################################
# CSV Inputs
## ###########################################################################

    def __loadCentroidsFromCSV(self):
        self.layers[Utils.LayersName.GPS] = Utils.createLayer('Point?crs='+Transforms.layer_proj, Utils.LayersName.GPS, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("lon", QVariant.Double), QgsField("lat", QVariant.Double)])
        self.layers[Utils.LayersName.MULTIPLT] = Utils.createLayer('MultiPoint?crs='+Transforms.layer_proj, Utils.LayersName.MULTIPLT, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int)])
        self.layers[Utils.LayersName.CONVEXHULL] = Utils.createLayer('Polygon?crs='+Transforms.layer_proj, Utils.LayersName.CONVEXHULL, [QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("area_m2", QVariant.Double), QgsField("angle_deg", QVariant.Double), QgsField("width_m", QVariant.Double), QgsField("height_m", QVariant.Double)])
        gps_coords = self.__csv2gps()
        self.__addGpsLayer(gps_coords)
        self.__computeCentroidsfromGPSCoords(gps_coords)
        QgsProject.instance().addMapLayer(self.layers[Utils.LayersName.GPS])
        QgsProject.instance().addMapLayer(self.layers[Utils.LayersName.MULTIPLT])
        QgsProject.instance().addMapLayer(self.layers[Utils.LayersName.CONVEXHULL])

    def __csv2gps(self):
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
                    Logger.logInfo("cluster_no_id")
                if c != 0:
                    line = re.split(',', g.strip())
                    gps_coords.append({
                        'cluster': line[cluster_no_id],
                        'type': line[cluster_type_id],
                        'lat': float(line[lat_id]),
                        'lon': float(line[lon_id])
                    })
                c = c + 1
        return gps_coords

    def __addGpsLayer(self, gps_coords):
        # add gps points to a layer
        for gps in gps_coords:
            point = QgsPointXY(gps['lon'], gps['lat'])
            gps_coords_ft = QgsFeature()
            gps_coords_ft.setGeometry(QgsGeometry.fromPointXY(point))
            gps_coords_ft.setAttributes([gps['cluster'], gps['type'], gps['lon'], gps['lat']])
            self.layers[Utils.LayersName.GPS].dataProvider().addFeatures([gps_coords_ft])

    def __computeCentroidsfromGPSCoords(self, gps_coords):
        unique_clusters = set(val['cluster'] for val in gps_coords)
        unique_clusters_with_type = []
        for unique_cluster in unique_clusters:
            cluster_type = sorted([val['type'] for val in gps_coords if val['cluster'] == unique_cluster])[0]
            unique_clusters_with_type.append(tuple((unique_cluster, cluster_type)))

        for cl in unique_clusters_with_type:
            self.__computeCentroid(cl, [val for val in gps_coords if val['cluster'] == cl[0]])

    def __computeCentroid(self, cluster, gps_coords_per_cluster):
        # compute gps coords list
        cluster_multipt_ft, gps_coords_list = self.__computeMultiptFeature(cluster, gps_coords_per_cluster)

        # compute convexhull
        cluster_convexhull_ft = self.__computeConvexhullFeature(cluster, gps_coords_list)

        # compute centroid
        cluster_centroid_ft = QgsFeature()
        cluster_centroid_ft.setAttributes([cluster[0], cluster[1], len(gps_coords_list)])
        self.__computeCentroidGeometry(cluster_centroid_ft, cluster_multipt_ft, cluster_convexhull_ft)
        self.layers[Utils.LayersName.CENTROIDS].dataProvider().addFeatures([cluster_centroid_ft])

    def __computeMultiptFeature(self, cluster, gps_coords_per_cluster):
        gps_coords_list = []
        for p in gps_coords_per_cluster:
            point = QgsPointXY(p['lon'], p['lat'])
            gps_coords_list.append(point)

        cluster_multipt_ft = QgsFeature()
        cluster_multipt_ft.setGeometry(QgsGeometry.fromMultiPointXY(gps_coords_list))
        cluster_multipt_ft.setAttributes([cluster[0], cluster[1], len(gps_coords_list)])
        self.layers[Utils.LayersName.MULTIPLT].dataProvider().addFeatures([cluster_multipt_ft])
        return cluster_multipt_ft, gps_coords_list

    def __computeConvexhullFeature(self, cluster, gps_coords_list):
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
        self.layers[Utils.LayersName.CONVEXHULL].dataProvider().addFeatures([cluster_convexhull_ft])

        return cluster_convexhull_ft

    def __computeCentroidGeometry(self, cluster_centroid_ft, cluster_multipt_ft, cluster_convexhull_ft):
        # determine if pole of inaccessibility can be determined
        if cluster_convexhull_ft.geometry().poleOfInaccessibility(100)[0].isNull():
            cluster_centroid_ft.setGeometry(cluster_multipt_ft.geometry().centroid())
        else:
            cluster_centroid_ft.setGeometry(cluster_convexhull_ft.geometry().poleOfInaccessibility(100)[0])
