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

from qgis.core import (QgsVectorLayer, QgsRasterLayer, QgsGeometry, QgsPoint, QgsPointXY, QgsField, QgsFeature, QgsRasterPipe, QgsRasterFileWriter, QgsVectorFileWriter, QgsProject, QgsCoordinateTransformContext) #, QgsRaster  # QGIS3
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
import math
import tempfile

from .Logger import Logger
from .Transforms import Transforms
from . import Utils

# to avoid GEOS errors! see: https://stackoverflow.com/questions/62075847/using-qgis-and-shaply-error-geosgeom-createlinearring-r-returned-a-null-pointer

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
        self.input_csv_field_nodata = None # can be null/empty, to catch

        self.images_directory = Path(self.input_csv).parent

        self.__ref_layer = None
        self.__ref_layer_shp = ""
        self.__ref_layer_id_field = ""

        self.output_file = ''
        self.output_warning = ''

####################################################################
# setters
####################################################################

    def setReferenceLayer(self, layer: QgsVectorLayer, layer_file: str, id_field: str = CLUSTER_N0_FIELD_NAME) -> typing.NoReturn:
        # TODO: could we extact the shp file from the layer properties and simplify parameters of the method? (provider.dataSourceUri()?)
        self.__ref_layer = layer
        self.__ref_layer_shp = layer_file
        self.__ref_layer_id_field = id_field

####################################################################
# computation
####################################################################

    def computeCovariates(self, progress_bar) -> typing.NoReturn:
        """ Facade that handle the covariates computation
        """
        # Generate output name
        output_filename = CovariatesProcesser.OUTPUT_SUFFIX_BASENAME
        if Utils.LayersName.basename:
            output_filename = Utils.LayersName.basename + '_' + CovariatesProcesser.OUTPUT_SUFFIX_BASENAME

        self.output_file = os.path.join(Utils.LayersName.outputDirectory, output_filename)

        Logger.logInfo("[CovariatesProcesser | STEP02 MANAGER] input_file:  " + self.input_csv)
        Logger.logInfo("[CovariatesProcesser | STEP02 MANAGER] input_csv_field_filename  :  " + self.input_csv_field_filename)
        Logger.logInfo("[CovariatesProcesser | STEP02 MANAGER] input_csv_field_fileformat:  " + self.input_csv_field_fileformat)
        Logger.logInfo("[CovariatesProcesser | STEP02 MANAGER] input_csv_field_sumstat   :  " + self.input_csv_field_sumstat)
        Logger.logInfo("[CovariatesProcesser | STEP02 MANAGER] input_csv_field_columnname:  " + self.input_csv_field_columnname)
        Logger.logInfo("[CovariatesProcesser | STEP02 MANAGER] input_csv_field_nodata:  " + (self.input_csv_field_nodata if self.input_csv_field_nodata else "None"))

        ref_layer_id_field = self.__ref_layer_id_field

        shortest_distance_basename = ""

        # read input list of covariates
        delimiter = Utils.detect_csv_delimiter(self.input_csv)
        Logger.logInfo(f"[CovariatesProcesser] Detected delimiter: '{delimiter}'")

        # multiple covariates can be defined in a single row, separated by ; or ,
        # each covariate must have a corresponding output column name
        covariate_delimiter = ';' if delimiter == ',' else ','
        
        with open(self.input_csv, "r", encoding='utf-8-sig') as f:

            qgis_project = QgsProject.instance()
            ref_features = [
                {
                    'fid': ft.id(),
                    ref_layer_id_field: ft[ref_layer_id_field]
                } for ft in self.__ref_layer.getFeatures()
            ]  # TODO: ft.id() is different than ft.GetFID()? !!!!! make sure IDs match - fix required!!!

            # Convert the dictionary into DataFrame
            summary_df = pd.DataFrame(ref_features)
            summary_df = summary_df.astype({ref_layer_id_field: "string"}) # force string type for the ID field

            # read all input covariates
            rowIndex = 0
            inputs = []
            expected_columns = None
            for i in f:
                if rowIndex == 0:

                    line = [s.strip() for s in re.split(re.escape(delimiter), i.strip())] # error here
                    expected_columns = len(line)
                    input_file_id = line.index(self.input_csv_field_filename)
                    input_fileformat_id = line.index(self.input_csv_field_fileformat)
                    input_field_sumstat_id = line.index(self.input_csv_field_sumstat)
                    input_field_columnname_id = line.index(self.input_csv_field_columnname)
                    input_field_nodata_id = line.index(self.input_csv_field_nodata) if self.input_csv_field_nodata else None
                if rowIndex != 0:
                    line = [s.strip() for s in re.split(re.escape(delimiter), i.strip())]
                    # Pad with empty strings if needed
                    if len(line) < expected_columns:
                        line += [''] * (expected_columns - len(line))

                    inputs.append({
                        'row_index': rowIndex,
                        'file': line[input_file_id],
                        'file_format': line[input_fileformat_id],
                        'sum_stats': line[input_field_sumstat_id].split(covariate_delimiter), # list of one or more summary stats
                        'column_names': line[input_field_columnname_id].split(covariate_delimiter), # list of one or more output columns
                        'user_nodata_value': line[input_field_nodata_id] if input_field_nodata_id else None
                    })

                rowIndex = rowIndex + 1
            
            total_rows = len(inputs)
            i = 0 # used only for progress bar
            # loop through all covariates
            for input_row in inputs:
                i += 1
                row_index = input_row['row_index']
                file_name = input_row['file']
                file_path = os.path.join(self.images_directory, file_name)
                file_format = input_row['file_format']
                sum_stats = input_row['sum_stats']
                column_names = input_row['column_names']
                user_nodata_value = None if not input_row['user_nodata_value'] or input_row['user_nodata_value'] == "" else input_row['user_nodata_value']

                if 'variety' in sum_stats:
                    msg_error = "Variety statistic is temporarily not supported in this version, it will not be available in the output file."
                    #Logger.logWarning(msg_error)
                    self.output_warning = msg_error
                    variety_index = sum_stats.index('variety')
                    sum_stats.remove('variety')
                    column_names.pop(variety_index)
                    if len(sum_stats) == 0:
                        progress_bar.update(int((i) / total_rows * 100))
                        continue
                
                if len(sum_stats) != len(column_names):
                    raise ValueError(f"In row {rowIndex+1} of the input CSV file, the number of summary statistics ({len(sum_stats)}) does not match the number of output columns ({len(column_names)}). Please correct the input file.")
                    
                # else:
                Logger.logInfo(f"[CovariatesProcesser] Processing input file row {row_index}: file name: {file_name} | file format: {file_format} | summary statistics: {str(sum_stats)}, | output columns: {str(column_names)} | user nodata value: {user_nodata_value}")

                # Compute distance to nearest
                if file_format == 'Shapefile':
                    if covariate_delimiter.join(sum_stats) == 'distance_to_nearest':

                        column_name = column_names[0]  # only one output column supported for distance to nearest

                        # create layer for shortest distance
                        shortest_distance_basename = file_name.split('.')[0]  # remove file extension
                        shortest_dist_lyr = QgsVectorLayer('LineString?crs=epsg:4326', f'Shortest distance to {shortest_distance_basename}', 'memory')
                        shortest_dist_prov = shortest_dist_lyr.dataProvider()
                        shortest_dist_prov.addAttributes([
                            QgsField(ref_layer_id_field, QtCore.QMetaType.Type.QString),
                            QgsField("nearestfid", QtCore.QMetaType.Type.QString),
                            QgsField("dist", QtCore.QMetaType.Type.Double, 'double', 15, 2)
                        ])
                        shortest_dist_lyr.updateFields()

                        layer = QgsVectorLayer(file_path, file_name, "ogr")
                        search_features = [feature for feature in layer.getFeatures()]
                        #crs_transformation = None
                        for cluster_ft in self.__ref_layer.getFeatures():
                            feat = QgsFeature()

                            startGeom = Utils.getPoleOfInaccessibilityOrCentroid(cluster_ft)
                            endGeom = QgsGeometry.fromPointXY(QgsPointXY(0, 0))

                            #if not crs_transformation:
                            # obtain the target transformation
                            startPoint = startGeom.asPoint() # QgsPointXY
                            crs_transformation = Transforms(startPoint.y(), startPoint.x())

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
                                    contains = geom.contains(startPoint)
                                    if contains:
                                        minDistFtId = tmp_ft.id()
                                        isInsideFeature = True
                                        break

                                if not isInsideFeature:
                                    cswc = min(
                                        [(
                                            l.id(), l.geometry().closestSegmentWithContext(startPoint)
                                        ) for l in search_features],
                                        key=itemgetter(1)
                                    )
                                    minDistPoint = cswc[1][1]  # nearest point on line
                                    minDistFtId = cswc[0]  # line id of nearest point
                                    endGeom = QgsGeometry.fromPointXY(QgsPointXY(minDistPoint[0], minDistPoint[1]))
                                else:
                                    endGeom = startGeom

                            line = QgsGeometry.fromPolyline([
                                QgsPoint(startPoint),
                                QgsPoint(endGeom.asPoint())
                            ])
                            # creating line between point and nearest point
                            feat.setGeometry(line)

                            # get distance in meters - transform to Web Mercator
                            line_merc = QgsGeometry(line)
                            line_merc.transform(crs_transformation.tr)

                            feat.setAttributes([
                                cluster_ft[ref_layer_id_field],
                                minDistFtId,
                                line_merc.length()
                            ])
                            shortest_dist_prov.addFeatures([feat])

                        # Update extent of the layer
                        shortest_dist_lyr.updateExtents()
                        # Add the layer to the Layers panel
                        qgis_project.addMapLayer(shortest_dist_lyr)

                        search_fts = [{ref_layer_id_field: ft[ref_layer_id_field], column_name: ft['dist']} for ft in
                                      shortest_dist_lyr.getFeatures()]
                        # Convert the dictionary into DataFrame
                        search_shp_df = pd.DataFrame(search_fts, columns=[ref_layer_id_field, column_name])
                        search_shp_df = search_shp_df.astype({ref_layer_id_field: "string"}) # force string type for the ID field

                        summary_df = pd.merge(
                            summary_df,
                            search_shp_df[[column_name, ref_layer_id_field]],
                            on=ref_layer_id_field,
                            how='inner'
                        )

                    else:
                        msg_error = f"Shapefile covariate supports only 'distance_to_nearest' summary statistic, '{str(sum_stats)}' is not supported and will not be available in the output file."
                        self.output_warning = msg_error
                        progress_bar.update(int((i) / total_rows * 100))
                        continue
                
                # Compute zonal stats and geotiff
                elif file_format == 'GeoTIFF':
                    column_prefix = '_'
                    # https://mapscaping.com/nodata-values-in-rasters-with-qgis/
                    stats_df = self.zonal_stat(
                        stats=sum_stats, # list of one or more summary stats
                        vector_path=self.__ref_layer_shp,
                        raster_path=file_path,
                        raster_band=1,
                        user_nodata_value=user_nodata_value,
                        column_prefix=column_prefix,
                        cluster_no_field=ref_layer_id_field
                    )
                    
                    outcols = [*[f'{column_prefix}{stat_name}' for stat_name in sum_stats], ref_layer_id_field]
                    results_df = stats_df[outcols]
                    results_df.columns = [*column_names, ref_layer_id_field]
                    results_df = results_df.astype({ref_layer_id_field: "string"}) # force string type for the ID field

                    summary_df = pd.merge(
                        summary_df,  # merge destination
                        results_df[[*column_names, ref_layer_id_field]],
                        on=ref_layer_id_field,
                        how='inner'
                    )
                
                else:
                    msg_error = f"Unknown file format '{file_format}' in row {row_index+1} of the input CSV file, it must be either 'Shapefile' or 'GeoTIFF'. The covariate will not be available in the output file."
                    self.output_warning = msg_error
                    progress_bar.update(int((i) / total_rows * 100))
                    continue

                progress_bar.update(int((i) / total_rows * 100))

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

        Logger.logInfo("[CovariatesProcesser] Output file saved to {}".format(self.output_file))
        Logger.logInfo("[CovariatesProcesser] Successfully completed at {}".format(datetime.now()))

    ####################################################################
    # Utilitity method
    ####################################################################

    def bbox_to_pixel_offsets(self, gt, bbox):
        '''Compute bbox to pixel offsets
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
            stats,
            vector_path,
            raster_path,
            raster_band = 1,
            user_nodata_value = None,
            column_prefix = '_',
            cluster_no_field = CLUSTER_N0_FIELD_NAME,
            global_src_extent = False
            ):
        '''Compute zonal statistic
        '''

        def is_equal_nodata_value(value, nodata_value):
            """Check if the value is equal to the nodata value, considering floating point precision issues."""
            if nodata_value is None or value is None:
                return False
            float_limit_number = -3.40282347e+38 # maximum negative value representable in single-precision floating-point format (float32), common as nodata value : equal operator doesn't work with it, we need math.isclose()
            if math.isclose(nodata_value, float_limit_number, rel_tol=1e-7):
                return math.isclose(value, nodata_value, rel_tol=1e-7)
            else:
                return value == nodata_value

        def exists_data_value(list, nodata_value):
            exists = False
            float_limit_number = -3.40282347e+38 # maximum negative value representable in single-precision floating-point format (float32), common as nodata value : equal operator doesn't work with it, we need math.isclose()
            
            if math.isclose(nodata_value, float_limit_number, rel_tol=1e-7):
                
                if any(
                    any(not math.isclose(value, nodata_value, rel_tol=1e-7) for value in sublist)
                    for sublist in list
                ):
                    #print('valid data value found in list - 1')
                    exists = True

            elif any(not nodata_value in sublist for sublist in list):
                #print('nodata_value found in list - 2')
                exists = True

            return exists
        
        Logger.logInfo(f"[CovariatesProcesser] Processing {stats}...")
        #print(f"[CovariatesProcesser] Processing {stats}...")

        if not os.path.isfile(vector_path):
            Logger.logInfo("[CovariatesProcesser | ZonalStat] vector dataset is missing")
            Logger.logInfo("[CovariatesProcesser | ZonalStat] vector_path path was: " + vector_path)

        if not os.path.isfile(raster_path):
            Logger.logInfo("[CovariatesProcesser | ZonalStat] raster dataset is missing")
            Logger.logInfo("[CovariatesProcesser | ZonalStat] raster_path path was: " + raster_path)     

        has_yes_or_no = False
        if 'yes_or_no' in stats:

            has_yes_or_no = True

            yes_or_no_field = f'{column_prefix}yes_or_no'

            rds = gdal.Open(raster_path, GA_ReadOnly)
            assert rds

            rb = rds.GetRasterBand(1)
            rgt = rds.GetGeoTransform()

            original_raster_nodata_value = rb.GetNoDataValue()

            Logger.logInfo(f"[CovariatesProcesser | ZonalStat | yes_or_no] Raster properties: nodata (GDAL)={original_raster_nodata_value}")
            Logger.logInfo(f"[CovariatesProcesser | ZonalStat | yes_or_no] User input: nodata={user_nodata_value}")
            
            if original_raster_nodata_value is None and user_nodata_value is None:
                raise ValueError(f"Raster nodata value is not set, please provide a valid nodata value in the input file or set the raster's nodata value in the raster properties.")

            if user_nodata_value and not is_equal_nodata_value(original_raster_nodata_value, float(user_nodata_value)):
                # overwrite the raster nodata value with the user provided value
                Logger.logInfo('[CovariatesProcesser | ZonalStat | yes_or_no] Overwriting raster nodata value with user provided value...')
                raster_nodata_value = float(user_nodata_value)
                rb.SetNoDataValue(raster_nodata_value)
            else:
                # else keeps original raster nodata value
                raster_nodata_value = original_raster_nodata_value

            Logger.logInfo(f"[CovariatesProcesser | ZonalStat | yes_or_no] Used: nodata={raster_nodata_value}")

            vds = ogr.Open(vector_path, GA_ReadOnly)
            if not vds:
                Logger.logInfo("[CovariatesProcesser | ZonalStat | yes_or_no] vds is missing")
                Logger.logInfo("[CovariatesProcesser | ZonalStat | yes_or_no] vector_path path was: " + vector_path)

            vlyr = vds.GetLayer(0)

            # Loop through vectors
            featureset_stats = []
            feat = vlyr.GetNextFeature()

            while feat is not None:
                # print('feat[cluster_no_field]: ' + str(feat[cluster_no_field]))

                if not global_src_extent: # this is always False as long as the zonal_stats function keeps the default value
                    # use local source extent
                    # fastest option when you have fast disks and well indexed raster (ie tiled Geotiff)
                    # advantage: each feature uses the smallest raster chunk
                    # disadvantage: lots of reads on the source raster
                    src_offset = self.bbox_to_pixel_offsets(rgt, feat.geometry().GetEnvelope())
                    src_array = rb.ReadAsArray(*src_offset)
                    
                    # print('src_array:')
                    # print(src_array)
                    # print('')

                yes_or_no = 'Yes' if exists_data_value(src_array, raster_nodata_value) else 'No'
                # print('yes_or_no: ' + yes_or_no)

                feature_stats = {
                    cluster_no_field: feat[cluster_no_field],
                    yes_or_no_field: yes_or_no
                }
                
                featureset_stats.append(feature_stats)
                feat = vlyr.GetNextFeature()
                # print('')

            vds = None
            rds = None

            yes_or_no_df = pd.DataFrame(featureset_stats)[[yes_or_no_field, cluster_no_field]]
            Logger.logInfo(f"[CovariatesProcesser | ZonalStat | yes_or_no] yes_or_no computed.")

            if len(stats) == 1: # there is no other stat than yes_or_no
                return yes_or_no_df

        #else:
        if (has_yes_or_no and len(stats) > 1) or (not has_yes_or_no and len(stats) >= 1):
            # other stats than yes_or_no

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
                '10': 'variety', # phase1: exclude from options, phase2: workaround to overcome QGIS bug - calculate all stats at once for a raster
                '11': 'variance'
            }

            def get_stat_id(stat_name):
                """Get the stat id from the stat name
                """
                if stat_name == 'yes_or_no':
                    return # not used in this function
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

            # Load original raster
            layer = QgsRasterLayer(raster_path, "tmp_raster", "gdal")
            if not layer.isValid():
                raise Exception(f"Raster could not be loaded: {raster_path}")

            provider = layer.dataProvider()

            # Check the current nodata value
            current_nodata = provider.sourceNoDataValue(1)
            Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] Raster properties: nodata={current_nodata}")
            Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] User input: nodata={user_nodata_value}")

            # Flag to know if we need the temporal raster
            if user_nodata_value is None:
                use_temporal = False
            else:
                user_nodata_value = float(user_nodata_value)
                use_temporal = not (is_equal_nodata_value(current_nodata, user_nodata_value))

            # Define input raster based on use_temporal
            if not use_temporal:
                input_raster = raster_path
                tmpfile = None
                Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] Using original raster with its own nodata value.")
                # if user_nodata_value is None:
                #     Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] Using original raster with its current nodata value.")
                # else:
                #     Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] Current nodata value matches with the value given by the user.") #, temporal raster is not generated.")
            else:
                Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] Nodata values do not match, creating temporal raster with the user nodata value...")

                # Redefine nodata
                provider.setNoDataValue(1, user_nodata_value)

                # Save to temporal file
                tmpdir = tempfile.gettempdir() # TODO: use plugins output directory
                tmpfile = os.path.join(tmpdir, "tmp_raster_corr.tif")

                pipe = QgsRasterPipe()
                if not pipe.set(provider.clone()):
                    raise Exception("Could not clone the dataProvider to the pipe.")
                
                writer = QgsRasterFileWriter(tmpfile)
                writer.writeRaster(
                    pipe,
                    layer.width(),
                    layer.height(),
                    layer.extent(),
                    layer.crs()
                )
                input_raster = tmpfile
            
            try:

                stat_index_list = [get_stat_id(stat_name) for stat_name in stats if get_stat_id(stat_name) is not None] # exclude None values (yes_or_no)

                result = processing.run("native:zonalstatisticsfb", {
                    'INPUT': vector_path,
                    'INPUT_RASTER': input_raster, #raster_path,
                    'RASTER_BAND': raster_band,
                    'COLUMN_PREFIX': column_prefix,
                    'STATISTICS': stat_index_list,
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
                Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] {str(stats)} computed.")

            finally:
                # Clean temporal raster if created
                if use_temporal and tmpfile and os.path.exists(tmpfile):
                    try:
                        os.remove(tmpfile)
                        Logger.logInfo(f"[CovariatesProcesser | ZonalStat | Raster] Temporal raster {tmpfile} deleted.")
                    except Exception as e:
                        Logger.logWarning(f"[CovariatesProcesser | ZonalStat | Raster] Temporal {tmpfile} could not be deleted: {e}")

            if has_yes_or_no:
                # merge with yes_or_no_df
                df = pd.merge(
                    df, # merge destination
                    yes_or_no_df[[yes_or_no_field, cluster_no_field]],
                    on=cluster_no_field,
                    how='inner'
                )

            # Return a dataframe, unlike the original zonal_stats function (caution)
            return df

