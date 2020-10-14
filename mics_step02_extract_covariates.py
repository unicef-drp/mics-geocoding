from qgis.core import QgsProject #QGIS3
from qgis.PyQt.QtCore import QVariant
from pathlib import Path
import pandas as pd

import itertools
from operator import itemgetter

import geopandas as gpd
import numpy as np
import pandas as pd

from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString

# to avoid GEOS errors! see: https://stackoverflow.com/questions/62075847/using-qgis-and-shaply-error-geosgeom-createlinearring-r-returned-a-null-pointer
from shapely import speedups
speedups.disable()


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
from osgeo import gdal, ogr
from osgeo.gdalconst import *
import numpy as np
import sys
gdal.PushErrorHandler('CPLQuietErrorHandler')


def bbox_to_pixel_offsets(gt, bbox):
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


def zonal_stats(vector_path, raster_path, cluster_no_field, nodata_value=None, global_src_extent=False):
    rds = gdal.Open(raster_path, GA_ReadOnly)
    assert rds
    rb = rds.GetRasterBand(1)
    rgt = rds.GetGeoTransform()

    if nodata_value:
        nodata_value = float(nodata_value)
        rb.SetNoDataValue(nodata_value)

    vds = ogr.Open(vector_path, GA_ReadOnly)  # TODO maybe open update if we want to write stats
    assert vds
    vlyr = vds.GetLayer(0)

    # create an in-memory numpy array of the source raster data
    # covering the whole extent of the vector layer
    if global_src_extent:
        # use global source extent
        # useful only when disk IO or raster scanning inefficiencies are your limiting factor
        # advantage: reads raster data in one pass
        # disadvantage: large vector extents may have big memory requirements
        src_offset = bbox_to_pixel_offsets(rgt, vlyr.GetExtent())
        src_array = rb.ReadAsArray(*src_offset)

        # calculate new geotransform of the layer subset
        new_gt = (
            (rgt[0] + (src_offset[0] * rgt[1])),
            rgt[1],
            0.0,
            (rgt[3] + (src_offset[1] * rgt[5])),
            0.0,
            rgt[5]
        )

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
            src_offset = bbox_to_pixel_offsets(rgt, feat.geometry().GetEnvelope())
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
                src_array == nodata_value,
                np.logical_not(rv_array)
            )
        )

        feature_stats = {
            'min': float(masked.min()),
            'mean': float(masked.mean()),
            'max': float(masked.max()),
            'std': float(masked.std()),
            'sum': float(masked.sum()),
            'count': int(masked.count()),
            'cluster': feat[cluster_no_field],
            'fid': int(feat.GetFID())}

        stats.append(feature_stats)

        rvds = None
        mem_ds = None
        feat = vlyr.GetNextFeature()

    vds = None
    rds = None
    return stats

ref_lyr_name = 'civ_cluster_buffers'
# add ref areas to spatial index
ref_lyr = [layer for layer in QgsProject.instance().mapLayers().values() if layer.name() == ref_lyr_name][0]
ref_shp = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2020\MICS geocoding\Covariates\civ_cluster_buffers.shp'
cluster_no_field_name = 'cluster'

input_csv = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2020\MICS geocoding\Covariates\_input_covariates.txt'
input_field_filename = 'FileName'
input_field_fileformat = 'FileFormat'
input_field_sumstat = 'SummaryStatistic'
input_field_columnname = 'ColumnName'
basefolder = Path(input_csv).parent

f = open(input_csv, "r")
c = 0
inputs = []

clusters = [{'fid':ft.id(), 'cluster':ft['cluster']} for ft in ref_lyr.getFeatures()]  # TODO: ft.id() is different than ft.GetFID()? !!!!! make sure IDs match - fix required!!!
# Convert the dictionary into DataFrame
summary_df = pd.DataFrame(clusters)


sourceCrs = QgsCoordinateReferenceSystem(4326)
destCrs = QgsCoordinateReferenceSystem(3857)
tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())

for i in f:
	if c == 0:
		line = re.split('\t', i.strip())
		input_file_id = line.index(input_field_filename)
		input_fileformat_id = line.index(input_field_fileformat)
		input_field_sumstat_id = line.index(input_field_sumstat)
		input_field_columnname_id = line.index(input_field_columnname)
	if c != 0:
		line = re.split('\t', i.strip())
		inputs.append({'file': line[input_file_id], 'format': line[input_fileformat_id], 'sum_stat': line[input_field_sumstat_id], 'column': line[input_field_columnname_id]})
	c = c + 1

for input in inputs:
	file_name = input['file']
	file_path = os.path.join(basefolder, file_name)
	format = input['format']
	sum_stat = input['sum_stat']
	column_name = input['column']
	# if format == 'GeoTIFF':
	# 	stats = zonal_stats(ref_shp,file_path,'cluster',-99999)
	# 	results_df = pd.DataFrame(stats)[[sum_stat, 'fid', 'cluster']]
	# 	results_df.columns = [column_name, 'fid', 'cluster_orig']
	# 	# summary_df.join(results_df,'fid')
	# 	summary_df = pd.merge(summary_df, results_df[[column_name, 'fid', 'cluster_orig']], on='fid', how='left')
	if format == 'Shapefile':
		search_gdf = gpd.read_file(file_path)
		if sum_stat == 'distance_to_nearest':
			# create layer for shortest distance
			shortest_dist_lyr = QgsVectorLayer('LineString?crs=epsg:4326', 'Shortest distance to {}'.format(file_name), 'memory')
			shortest_dist_prov = shortest_dist_lyr.dataProvider()
			shortest_dist_prov.addAttributes(
				[QgsField("cluster_id", QVariant.String), QgsField("nearestfid", QVariant.String),
				 QgsField("dist", QVariant.Double)])
			shortest_dist_lyr.updateFields()

			layer = QgsVectorLayer(file_path, file_name, "ogr")
			search_features = [feature for feature in layer.getFeatures()]
			for cluster_ft in ref_lyr.getFeatures():
				cswc = min(
					[(l.id(), l.geometry().closestSegmentWithContext(cluster_ft.geometry().centroid().asPoint())) for l in
					 search_features], key=itemgetter(1))
				# cswc = min([(s.id(), s.geometry().closestSegmentWithContext(QgsPoint(cluster_ft.geometry().centroid().asPoint()))) for s in search_features], key=itemgetter(1))
				minDistPoint = cswc[1][1]  # nearest point on line
				minDistLine = cswc[0]  # line id of nearest point
				feat = QgsFeature()
				line = QgsGeometry.fromPolyline([QgsPoint(cluster_ft.geometry().centroid().asPoint()), QgsPoint(minDistPoint[0], minDistPoint[1])])  # creating line between point and nearest point on segment
				feat.setGeometry(line)

				# get distance in meters - transform to Web Mercator
				line_merc = QgsGeometry(line)
				line_merc.transform(tr)

				feat.setAttributes([cluster_ft.id(), minDistLine, line_merc.length()])
				shortest_dist_prov.addFeatures([feat])

			# Update extent of the layer
			shortest_dist_lyr.updateExtents()
			# Add the layer to the Layers panel
			registry.addMapLayer(shortest_dist_lyr)
