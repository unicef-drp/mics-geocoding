## ###########################################################################
##
# CovariatesProcesser.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

from qgis.core import (QgsVectorLayer, QgsRasterLayer, QgsGeometry, QgsPoint, QgsPointXY, QgsField, QgsFeature, QgsVectorFileWriter, QgsProject, QgsCoordinateTransformContext) #, QgsRaster  # QGIS3
from qgis import processing
from PyQt5 import QtCore

from osgeo.gdalconst import GA_ReadOnly
from osgeo import gdal, ogr
import os
import re
import typing
from pathlib import Path
from datetime import datetime
from operator import itemgetter
import numpy as np
import pandas as pd

from .Logger import Logger
from .Transforms import Transforms
from . import Utils

# to avoid GEOS errors! see: https://stackoverflow.com/questions/62075847/using-qgis-and-shaply-error-geosgeom-createlinearring-r-returned-a-null-pointer
# This might be useless - I tried without it an it worked fine
#from shapely import speedups
#speedups.disable()

"""
Zonal Statistics
Vector-Raster Analysis
Copyright 2013 Matthew Perry
Usage:
  zonal_stats.py VECTOR RASTER
  zonal_stats.py -h | --help
  zonal_stats.py --version
Options:
  -h --help     Show this screen.
  --version     Show version.
"""
gdal.PushErrorHandler('CPLQuietErrorHandler')


####################################################################
# Class CovariatesProcesser
####################################################################

class CovariatesProcesser():
    """ Facade that handle step 2 of the algo.
        set inputs, call loader and displacef with proper arguments.
    """
    OUTPUT_SUFFIX_BASENAME = "output_covariates.csv"
    CLUSTER_N0_FIELD_NAME = "cluster"

    def __init__(self):
        # CSV input
        self.input_csv = ""
        self.input_csv_field_filename = ''
        self.input_csv_field_fileformat = ''
        self.input_csv_field_sumstat = ''
        self.input_csv_field_columnname = ''

        self.images_directory = Path(self.input_csv).parent

        self.__ref_layer = None
        self.__ref_layer_shp = ""

        self.output_file = ''

####################################################################
# setters
####################################################################

    def setReferenceLayer(self, layer: QgsVectorLayer, layer_file: str) -> typing.NoReturn:
        # TODO: could we extact the shp file from the layer properties and simplify parameters of the method? (provider.dataSourceUri()?)
        self.__ref_layer = layer
        self.__ref_layer_shp = layer_file

####################################################################
# computation
####################################################################

    def computeCovariates(self) -> typing.NoReturn:
        """ Facade that handle the covariates computation
        """
        # Generate output name
        output_filename = CovariatesProcesser.OUTPUT_SUFFIX_BASENAME
        if Utils.LayersName.basename:
            output_filename = Utils.LayersName.basename + '_' + CovariatesProcesser.OUTPUT_SUFFIX_BASENAME

        self.output_file = os.path.join(Utils.LayersName.outputDirectory, output_filename)

        Logger.logInfo("[STEP02 MANAGER] input_file:  " + self.input_csv)
        Logger.logInfo("[STEP02 MANAGER] input_csv_field_filename  :  " + self.input_csv_field_filename)
        Logger.logInfo("[STEP02 MANAGER] input_csv_field_fileformat:  " + self.input_csv_field_fileformat)
        Logger.logInfo("[STEP02 MANAGER] input_csv_field_sumstat   :  " + self.input_csv_field_sumstat)
        Logger.logInfo("[STEP02 MANAGER] input_csv_field_columnname:  " + self.input_csv_field_columnname)

        shortest_distance_basename = ""

        # read input list of covariates
        with open(self.input_csv, "r", encoding='utf-8-sig') as f:
            rowIndex = 0
            inputs = []

            registry = QgsProject.instance()

            clusters = [
                {
                    'fid': ft.id(),
                    CovariatesProcesser.CLUSTER_N0_FIELD_NAME: ft[CovariatesProcesser.CLUSTER_N0_FIELD_NAME]
                } for ft in self.__ref_layer.getFeatures()
            ]  # TODO: ft.id() is different than ft.GetFID()? !!!!! make sure IDs match - fix required!!!

            # Convert the dictionary into DataFrame
            summary_df = pd.DataFrame(clusters)

            # read all input covariates
            for i in f:
                if rowIndex == 0:
                    line = [s.strip() for s in re.split(',', i.strip())]
                    input_file_id = line.index(self.input_csv_field_filename)
                    input_fileformat_id = line.index(self.input_csv_field_fileformat)
                    input_field_sumstat_id = line.index(self.input_csv_field_sumstat)
                    input_field_columnname_id = line.index(self.input_csv_field_columnname)
                if rowIndex != 0:
                    line = [s.strip() for s in re.split(',', i.strip())]
                    inputs.append({
                        'file': line[input_file_id],
                        'file_format': line[input_fileformat_id],
                        'sum_stat': line[input_field_sumstat_id],
                        'column': line[input_field_columnname_id]
                    })
                rowIndex = rowIndex + 1
            rowIndex = 1

            # loop through all covariates
            for input_row in inputs:
                file_name = input_row['file']
                file_path = os.path.join(self.images_directory, file_name)
                file_format = input_row['file_format']
                sum_stat = input_row['sum_stat']
                column_name = input_row['column']
                Logger.logInfo("Processing input file no {}: file name: {}, file format: {}, summary statistics: {}, output column: {}".format(rowIndex, file_name, file_format, sum_stat, column_name))
                rowIndex = rowIndex + 1

                # Compute distance to nearest
                if file_format == 'Shapefile':
                    if sum_stat == 'distance_to_nearest':
                        # create layer for shortest distance
                        shortest_distance_basename = file_name
                        shortest_dist_lyr = QgsVectorLayer('LineString?crs=epsg:4326', 'Shortest distance to {}'.format(shortest_distance_basename), 'memory')
                        shortest_dist_prov = shortest_dist_lyr.dataProvider()
                        shortest_dist_prov.addAttributes([
                            QgsField("cluster", QtCore.QVariant.Int),
                            QgsField("nearestfid", QtCore.QVariant.String),
                            QgsField("dist", QtCore.QVariant.Double, 'double', 15, 2)
                        ])
                        shortest_dist_lyr.updateFields()

                        layer = QgsVectorLayer(file_path, file_name, "ogr")
                        search_features = [feature for feature in layer.getFeatures()]
                        #crs_transformation = None
                        for cluster_ft in self.__ref_layer.getFeatures():
                            feat = QgsFeature()
                            # startPt = QgsPoint(cluster_ft.geometry().centroid().asPoint())
                            startGeom = cluster_ft.geometry().centroid()
                            # endPt = QgsPoint(QgsPointXY(0, 0))
                            endGeom = QgsGeometry.fromPointXY(QgsPointXY(0, 0))

                            #if not crs_transformation:
                            # obtain the target transformation
                            pt = startGeom.asPoint() # QgsPointXY
                            crs_transformation = Transforms(pt.y(), pt.x())

                            minDistFtId = -1

                            if layer.geometryType() == 0:  # for point input shapefile
                                distance = -99
                                for nf in search_features:
                                    nfGeom = nf.geometry()
                                    new_distance = startGeom.distance(nfGeom)

                                    if distance < 0 or new_distance < distance:
                                        distance = new_distance
                                        closest_point = nfGeom.nearestPoint(startGeom)
                                        minDistFtId = nf.id()
                                endGeom = closest_point

                            elif layer.geometryType() in (1, 2):  # for line (1) / polygon (2) input shapefile
                                isInsideFeature = False
                                for tmp_ft in search_features:
                                    geom = tmp_ft.geometry()
                                    pt = cluster_ft.geometry().centroid().asPoint()
                                    contains = geom.contains(pt)
                                    if contains:
                                        minDistFtId = tmp_ft.id()
                                        isInsideFeature = True
                                        break

                                if not isInsideFeature:
                                    cswc = min(
                                        [(
                                            l.id(), l.geometry().closestSegmentWithContext(cluster_ft.geometry().centroid().asPoint())
                                        ) for l in search_features],
                                        key=itemgetter(1)
                                    )
                                    minDistPoint = cswc[1][1]  # nearest point on line
                                    minDistFtId = cswc[0]  # line id of nearest point
                                    # endPt = QgsPoint(minDistPoint[0], minDistPoint[1])
                                    endGeom = QgsGeometry.fromPointXY(QgsPointXY(minDistPoint[0], minDistPoint[1]))
                                else:
                                    endGeom = startGeom

                            line = QgsGeometry.fromPolyline([
                                QgsPoint(startGeom.asPoint()),
                                QgsPoint(endGeom.asPoint())
                            ])
                            # creating line between point and nearest point
                            feat.setGeometry(line)

                            # get distance in meters - transform to Web Mercator
                            line_merc = QgsGeometry(line)
                            line_merc.transform(crs_transformation.tr)

                            feat.setAttributes([
                                cluster_ft[CovariatesProcesser.CLUSTER_N0_FIELD_NAME],
                                minDistFtId,
                                line_merc.length()
                            ])
                            shortest_dist_prov.addFeatures([feat])

                        # Update extent of the layer
                        shortest_dist_lyr.updateExtents()
                        # Add the layer to the Layers panel
                        registry.addMapLayer(shortest_dist_lyr)

                        search_fts = [{CovariatesProcesser.CLUSTER_N0_FIELD_NAME: ft[CovariatesProcesser.CLUSTER_N0_FIELD_NAME], column_name: ft['dist']} for ft in
                                      shortest_dist_lyr.getFeatures()]
                        # Convert the dictionary into DataFrame
                        search_shp_df = pd.DataFrame(search_fts)
                        summary_df = pd.merge(
                            summary_df,
                            search_shp_df[[column_name, CovariatesProcesser.CLUSTER_N0_FIELD_NAME]],
                            on=CovariatesProcesser.CLUSTER_N0_FIELD_NAME,
                            how='inner'
                        )

                # Compute zonal stat and geotiff
                elif file_format == 'GeoTIFF':
                    column_prefix = '_'
                    # https://mapscaping.com/nodata-values-in-rasters-with-qgis/
                    #raster_nodata_value = -200 # TODO: set as user input
                    stats = self.zonal_stat(
                        stat=sum_stat,
                        vector_path=self.__ref_layer_shp,
                        raster_path=file_path,
                        raster_band=1,
                        #raster_nodata_value = raster_nodata_value,
                        column_prefix=column_prefix,
                        cluster_no_field=CovariatesProcesser.CLUSTER_N0_FIELD_NAME
                    )
                    
                    results_df = stats[[f'{column_prefix}{sum_stat}', CovariatesProcesser.CLUSTER_N0_FIELD_NAME]]
                    results_df.columns = [column_name, CovariatesProcesser.CLUSTER_N0_FIELD_NAME]
                    summary_df = pd.merge(
                        summary_df,  # merge destination
                        results_df[[column_name, CovariatesProcesser.CLUSTER_N0_FIELD_NAME]],
                        on=CovariatesProcesser.CLUSTER_N0_FIELD_NAME,
                        how='inner'
                    )

            # iterating the columns
            selected_columns = []
            excluded_columns = ["fid"]
            for col in summary_df.columns:
                if not col in excluded_columns:
                    selected_columns.append(col)

            summary_df.to_csv(
                self.output_file,
                sep=',',
                encoding='utf-8',
                index=False,
                columns=selected_columns
            )

            if shortest_distance_basename:
                # Rewrite the layer on disk -> no memory flag
                layerName = 'Shortest distance to {}'.format(shortest_distance_basename)
                layers = QgsProject.instance().mapLayersByName(layerName)
                if layers:
                    filename = Utils.LayersName.customfileName(layerName)
                    options = QgsVectorFileWriter.SaveVectorOptions()
                    options.driverName = "ESRI Shapefile"
                    writer = QgsVectorFileWriter.writeAsVectorFormatV2(
                        layers[0],
                        filename,
                        QgsCoordinateTransformContext(),
                        options)
                    Utils.removeLayerIfExistsByName(layerName)
                    layer = QgsVectorLayer(filename, layerName)
                    QgsProject.instance().addMapLayer(layer)

        Logger.logInfo("Output file saved to {}".format(self.output_file))
        Logger.logInfo("Successfully completed at {}".format(datetime.now()))

    ####################################################################
    # Utilitity method
    ####################################################################

    def bbox_to_pixel_offsets(self, gt, bbox):
        '''Compute bboc to pixel offsets
        '''
        origin_x = gt[0]
        origin_y = gt[3]
        pixel_width = gt[1]
        pixel_height = gt[5]
        x1 = int((bbox[0] - origin_x) / pixel_width)
        x2 = int((bbox[1] - origin_x) / pixel_width) + 1

        y1 = int((bbox[3] - origin_y) / pixel_height)
        y2 = int((bbox[2] - origin_y) / pixel_height) + 1

        xsize = x2 - x1
        ysize = y2 - y1
        return x1, y1, xsize, ysize
    
    def zonal_stat(self,
            stat,
            vector_path,
            raster_path,
            raster_band=1,
            #raster_nodata_value = -9999,
            column_prefix='_',
            cluster_no_field=CLUSTER_N0_FIELD_NAME,
            global_src_extent=False
            ):
        '''Compute zonal statistic
        '''

        DEFAULT_RASTER_NODATA_VALUE = -9999

        if not os.path.isfile(vector_path):
            Logger.logInfo("[ZonalStat] vector dataset is missing")
            Logger.logInfo("[ZonalStat] vector_path path was: " + vector_path)

        if not os.path.isfile(raster_path):
            Logger.logInfo("[ZonalStat] raster dataset is missing")
            Logger.logInfo("[ZonalStat] raster_path path was: " + raster_path)     

        if stat == 'yes_or_no':

            yes_or_no_field = f'{column_prefix}yes_or_no'

            rds = gdal.Open(raster_path, GA_ReadOnly)
            assert rds

            rb = rds.GetRasterBand(1)
            rgt = rds.GetGeoTransform()

            raster_nodata_value = rb.GetNoDataValue()

            if raster_nodata_value is None:
                raster_nodata_value = float(DEFAULT_RASTER_NODATA_VALUE)
                rb.SetNoDataValue(raster_nodata_value)

            Logger.logInfo(f"[ZonalStat] raster nodata value: {raster_nodata_value}")

            vds = ogr.Open(vector_path, GA_ReadOnly)  # TODO maybe open update if we want to write stats
            if not vds:
                Logger.logInfo("[ZonalStat] vds is missing")
                Logger.logInfo("[ZonalStat] vector_path path was: " + vector_path)

            vlyr = vds.GetLayer(0)

            mem_drv = ogr.GetDriverByName('Memory')
            driver = gdal.GetDriverByName('MEM')

            # Loop through vectors
            stats = []
            feat = vlyr.GetNextFeature()

            while feat is not None:

                if not global_src_extent:
                    # use local source extent
                    # fastest option when you have fast disks and well indexed raster (ie tiled Geotiff)
                    # advantage: each feature uses the smallest raster chunk
                    # disadvantage: lots of reads on the source raster
                    src_offset = self.bbox_to_pixel_offsets(rgt, feat.geometry().GetEnvelope())
                    src_array = rb.ReadAsArray(*src_offset)

                    # calculate new geotransform of the feature subset
                    new_gt = (
                        (rgt[0] + (src_offset[0] * rgt[1])),
                        rgt[1],
                        0.0,
                        (rgt[3] + (src_offset[1] * rgt[5])),
                        0.0,
                        rgt[5]
                    )

                # Create a temporary vector layer in memory
                mem_ds = mem_drv.CreateDataSource('out')
                mem_layer = mem_ds.CreateLayer('poly', None, ogr.wkbPolygon)
                mem_layer.CreateFeature(feat.Clone())

                # Rasterize it
                rvds = driver.Create('', src_offset[2], src_offset[3], 1, gdal.GDT_Byte)
                rvds.SetGeoTransform(new_gt)
                gdal.RasterizeLayer(rvds, [1], mem_layer, burn_values=[1])
                rv_array = rvds.ReadAsArray()

                # Mask the source data array with our current feature
                # we take the logical_not to flip 0<->1 to get the correct mask effect
                # we also mask out nodata values explictly
                masked = np.ma.MaskedArray(
                    src_array,
                    mask=np.logical_or(
                        src_array == raster_nodata_value,
                        np.logical_not(rv_array)
                    )
                )

                feature_stats = {
                    cluster_no_field: feat[cluster_no_field],
                    #'fid': int(feat.GetFID()),
                    yes_or_no_field: "Yes"
                }

                # get the actual pixel value for all stats if mask is returning null (e.g. pixel size is too large)
                if not masked.min():
                    geom = feat.geometry()
                    mx, my = geom.Centroid().GetX(), geom.Centroid().GetY()  # coord in map units

                    # Convert from map to pixel coordinates.
                    # Only works for geotransforms with no rotation.
                    px = int((mx - rgt[0]) / rgt[1])  # x pixel
                    py = int((my - rgt[3]) / rgt[5])  # y pixel

                    intval = rb.ReadAsArray(px, py, 1, 1)

                    yes_or_no = "Yes"
                    if intval == raster_nodata_value:
                        yes_or_no = "No"

                    feature_stats = {
                        cluster_no_field: feat[cluster_no_field],
                        #'fid': int(feat.GetFID()),
                        yes_or_no_field: yes_or_no
                    }

                stats.append(feature_stats)

                rvds = None
                mem_ds = None
                feat = vlyr.GetNextFeature()

            vds = None
            rds = None

            results_df = pd.DataFrame(stats)[[yes_or_no_field, cluster_no_field]]

            return results_df                

        else:
            stat_dict = {
                '0' : 'count',
                '1' : 'sum',
                '2' : 'mean',
                '3' : 'median',
                '4' : 'stdev',
                '5' : 'min',
                '6' : 'max',
                '7' : 'range',
                '8' : 'minority',
                '9' : 'majority',
                '10': 'variety',
                '11': 'variance'
            }

            def get_stat_id(stat_name):
                """Get the stat id from the stat name
                """
                for key, value in stat_dict.items():
                    if value == stat_name:
                        return int(key)
                raise ValueError(f"Unknown statistic name: {stat_name}")

            # Set new nodata value for the raster
            #processing.run("gdal:translate", {
            #    'INPUT':raster_path,
            #    'TARGET_CRS':None,
            #    'NODATA':raster_nodata_value,
            #    'COPY_SUBDATASETS':False,
            #    'OPTIONS':None,
            #    'EXTRA':'',
            #    'DATA_TYPE':0,
            #    'OUTPUT':'TEMPORARY_OUTPUT'
            #})

            result = processing.run("native:zonalstatisticsfb", {
                'INPUT': vector_path,
                'INPUT_RASTER': raster_path,
                'RASTER_BAND': raster_band,
                'COLUMN_PREFIX': column_prefix,
                'STATISTICS': [get_stat_id(stat)],
                'OUTPUT': 'memory:' #'TEMPORARY_OUTPUT'
            })
            layer = result['OUTPUT']

            # In case we want to load the layer on the map:
            #layer.setName("output_covariates" + output)        
            #QgsProject.instance().addMapLayer(layer)

            # `layer` contains a table with the stat (column) for each feature (row)
            # cluster | buf_dist | mean

            # Get a list of field names
            fieldnames = [field.name() for field in layer.fields()] # to define dataframe columns

            # Get a list of attributes for each selected feature
            data = [f.attributes() for f in layer.getFeatures()]
            
            # Create a Pandas DataFrame
            df = pd.DataFrame(data, columns=fieldnames)

            # Return a dataframe, unlike the original zonal_stats function (caution)
            return df

