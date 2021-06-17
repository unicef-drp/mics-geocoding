import random
from qgis.core import QgsProject #QGIS3
from qgis.PyQt.QtCore import QVariant
from datetime import datetime
from pathlib import Path
from qgis.core import (
  QgsGeometry,
  QgsPoint,
  QgsPointXY,
  QgsWkbTypes,
  QgsProject,
  QgsFeatureRequest,
  QgsVectorLayer,
  QgsDistanceArea,
  QgsUnitTypes,
)

######################################
# CONFIG FOR SAMPLE 01
######################################
input_file_clusters = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2021\MICS\Sample data\Sample01\sample01_cluster_centroids.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
lat_field = 'Lat'  # column name with latitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'  # column name with longitude (WGS84) coordinate (must be double, not string)

urban_types = ['U']  # values form the cluster type column that belong to urban type
rural_types = ['R']  # values form the cluster type column that belong to rural type

ref_lyr_name = 'ago_admin2'  # name of the QGIS layer with admin boundaries
ref_id_field = 'GID_2'  # column name with a unique ID (e.g. pcode) for admin unit

######################################
# CONFIG FOR SAMPLE 02
######################################
input_file_clusters = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2021\MICS\Sample data\Sample02\sample02_cluster_polygons.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
lat_field = 'Lat'  # column name with latitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'  # column name with longitude (WGS84) coordinate (must be double, not string)

urban_types = ['U']  # values form the cluster type column that belong to urban type
rural_types = ['R']  # values form the cluster type column that belong to rural type

ref_lyr_name = 'ago_admin2'  # name of the QGIS layer with admin boundaries
ref_id_field = 'GID_2'  # column name with a unique ID (e.g. pcode) for admin unit


######################################
# CONFIG FOR SAMPLE 03
######################################
input_file_clusters = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2021\MICS\Sample data\Sample03\sample03_cluster_centroids_table.csv'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
lat_field = 'Lat'  # column name with latitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'  # column name with longitude (WGS84) coordinate (must be double, not string)

urban_types = ['U']  # values form the cluster type column that belong to urban type
rural_types = ['R']  # values form the cluster type column that belong to rural type

ref_lyr_name = 'ago_admin2'  # name of the QGIS layer with admin boundaries
ref_id_field = 'GID_2'  # column name with a unique ID (e.g. pcode) for admin unit


######################################
# CONFIG FOR SAMPLE 04
######################################
input_file_clusters = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2021\MICS\Sample data\Sample04\sample04_cluster_coordinates_pt.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
lat_field = 'Lat'  # column name with latitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'  # column name with longitude (WGS84) coordinate (must be double, not string)

urban_types = ['U']  # values form the cluster type column that belong to urban type
rural_types = ['R']  # values form the cluster type column that belong to rural type

ref_lyr_name = 'ago_admin2'  # name of the QGIS layer with admin boundaries
ref_id_field = 'GID_2'  # column name with a unique ID (e.g. pcode) for admin unit


######################################
# CONFIG FOR SAMPLE 05
######################################
input_file_clusters = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2021\MICS\Sample data\Sample05\sample05_cluster_polygons.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
lat_field = 'Lat'  # column name with latitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'  # column name with longitude (WGS84) coordinate (must be double, not string)

urban_types = ['U']  # values form the cluster type column that belong to urban type
rural_types = ['R']  # values form the cluster type column that belong to rural type

ref_lyr_name = 'fji_admin1'  # name of the QGIS layer with admin boundaries
ref_id_field = 'GID_1'  # column name with a unique ID (e.g. pcode) for admin unit


######################################
# CONFIG FOR SAMPLE 06
######################################
input_file_clusters = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2021\MICS\Sample data\Sample06\sample06_cluster_coordinates_tab.csv'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
lat_field = 'Lat'  # column name with latitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'  # column name with longitude (WGS84) coordinate (must be double, not string)

urban_types = ['U']  # values form the cluster type column that belong to urban type
rural_types = ['R']  # values form the cluster type column that belong to rural type

ref_lyr_name = 'ago_admin2'  # name of the QGIS layer with admin boundaries
ref_id_field = 'GID_2'  # column name with a unique ID (e.g. pcode) for admin unit


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


def displacepoint(x, y, max_distance=5000):
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
	if 90 < angle_degree_internal <= 270: x_offset *= -1
	if angle_degree_internal > 180: y_offset *= -1

	# Add the offset to the original coordinate (in meters)
	new_x_internal = x + x_offset
	new_y_internal = y + y_offset

	return new_x_internal, new_y_internal, distance_internal, angle_degree_internal


def getval(ft, field):
	if field:
		val = ft[field]
		if val:
			if isinstance(val, basestring):
				result = "{}".format(val.encode('UTF-8').decode('UTF-8').strip())  # ToDo: decode or encode???: val.encode('UTF-8').strip()
			else:
				result = "{}".format(val)
		else:
			result = ""
	else:
		result = ""
	return result


##################################
# READ LIST OF INPUT COORDINATES
##################################

# CREATE OUTPUT MEMORY LAYERS
# create layer for gps points
gps_coords_lyr = QgsVectorLayer('Point?crs=epsg:4326', 'GPS Cluster Points', 'memory')
gps_coords_prov = gps_coords_lyr.dataProvider()
gps_coords_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("lon", QVariant.Double), QgsField("lat", QVariant.Double)])
gps_coords_lyr.updateFields()

# create layer for multipoints
cluster_multipt_lyr = QgsVectorLayer('MultiPoint?crs=epsg:4326', 'Cluster Multi-Points', 'memory')
cluster_multipt_prov = cluster_multipt_lyr.dataProvider()
cluster_multipt_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int)])
cluster_multipt_lyr.updateFields()

# create layer for convex hulls
cluster_convexhull_lyr = QgsVectorLayer('Polygon?crs=epsg:4326', 'Cluster Convex Hulls', 'memory')
cluster_convexhull_prov = cluster_convexhull_lyr.dataProvider()
cluster_convexhull_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("area_m2", QVariant.Double), QgsField("angle_deg", QVariant.Double), QgsField("width_m", QVariant.Double), QgsField("height_m", QVariant.Double)])
cluster_convexhull_lyr.updateFields()

# create layer for centroids
cluster_centroid_lyr = QgsVectorLayer('Point?crs=epsg:4326', 'Cluster Centroids', 'memory')
cluster_centroid_prov = cluster_centroid_lyr.dataProvider()
cluster_centroid_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int)])
cluster_centroid_lyr.updateFields()

# create layer for displaced centroids
cluster_disp_centroid_lyr = QgsVectorLayer('Point?crs=epsg:4326', 'Cluster Displaced Centroids', 'memory')
cluster_disp_centroid_prov = cluster_disp_centroid_lyr.dataProvider()
cluster_disp_centroid_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("lon_orig", QVariant.Double), QgsField("lat_orig", QVariant.Double), QgsField("lon_disp", QVariant.Double), QgsField("lat_disp", QVariant.Double), QgsField("disp_dist_m", QVariant.Double), QgsField("disp_angle", QVariant.Double), QgsField("refar_id_b", QVariant.String), QgsField("refar_id_a", QVariant.String), QgsField("iter", QVariant.Int)])
cluster_disp_centroid_lyr.updateFields()

# create layer for anonymized displaced centroids
cluster_anonym_disp_centroid_lyr = QgsVectorLayer('Point?crs=epsg:4326', 'Cluster Anonymized Displaced Centroids', 'memory')
cluster_anonym_disp_centroid_prov = cluster_anonym_disp_centroid_lyr.dataProvider()
cluster_anonym_disp_centroid_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("lon_disp", QVariant.Double), QgsField("lat_disp", QVariant.Double)])
cluster_anonym_disp_centroid_lyr.updateFields()


# create layer for displacement links
cluster_centroid_disp_links_lyr = QgsVectorLayer('LineString?crs=epsg:4326', 'Cluster Displacement Links', 'memory')
cluster_centroid_disp_links_prov = cluster_centroid_disp_links_lyr.dataProvider()
cluster_centroid_disp_links_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("lon_orig", QVariant.Double), QgsField("lat_orig", QVariant.Double), QgsField("lon_disp", QVariant.Double), QgsField("lat_disp", QVariant.Double), QgsField("disp_dist_m", QVariant.Double), QgsField("disp_angle", QVariant.Double), QgsField("refar_id_b", QVariant.String), QgsField("refar_id_a", QVariant.String), QgsField("iter", QVariant.Int)])
cluster_centroid_disp_links_lyr.updateFields()

# create layer for buffers
cluster_disp_centroid_buffer_lyr = QgsVectorLayer('Polygon?crs=epsg:4326', 'Cluster Buffers', 'memory')
cluster_disp_centroid_buffer_prov = cluster_disp_centroid_buffer_lyr.dataProvider()
cluster_disp_centroid_buffer_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("count", QVariant.Int), QgsField("buf_dist", QVariant.Double)])
cluster_disp_centroid_buffer_lyr.updateFields()

# create layer for anonymized buffers
cluster_anonym_disp_centroid_buffer_lyr = QgsVectorLayer('Polygon?crs=epsg:4326', 'Cluster Anonymized Buffers', 'memory')
cluster_anonym_disp_centroid_buffer_prov = cluster_anonym_disp_centroid_buffer_lyr.dataProvider()
cluster_anonym_disp_centroid_buffer_prov.addAttributes([QgsField("cluster", QVariant.String), QgsField("type", QVariant.String), QgsField("buf_dist", QVariant.Double)])
cluster_anonym_disp_centroid_buffer_lyr.updateFields()

# add ref areas to spatial index
ref_lyr = [layer for layer in QgsProject.instance().mapLayers().values() if layer.name() == ref_lyr_name][0]
ref_fts_index = QgsSpatialIndex(ref_lyr.getFeatures())

# create layer for cluster polygons (for use if the input is shp not csv)
cluster_lyr = QgsVectorLayer(input_file_clusters, "Cluster Polygons", "ogr")

# define geographic and projected coordinate systems
sourceCrs = QgsCoordinateReferenceSystem(4326)
destCrs = QgsCoordinateReferenceSystem(3857)
tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())

# check type of input file: extension must be csv or shp
input_file_clusters_format = Path(input_file_clusters).suffix[1:]

rural_displaced_points = 0
cluster_centroid_fts = []

if input_file_clusters_format == "csv":
	f = open(input_file_clusters, "r", encoding='utf-8-sig')
	c = 0
	gps_coords = []

	for g in f:
		if c == 0:
			line = re.split(',', g.strip())
			cluster_no_id = line.index(cluster_no_field)
			cluster_type_id = line.index(cluster_type_field)
			lat_id = line.index(lat_field)
			lon_id = line.index(lon_field)
			print(cluster_no_id)
		if c != 0:
			line = re.split(',', g.strip())
			gps_coords.append(
				{'cluster': line[cluster_no_id], 'type': line[cluster_type_id], 'lat': float(line[lat_id]),
				 'lon': float(line[lon_id])})
		c = c + 1

	# add gps points to a layer
	for gps in gps_coords:
		point = QgsPointXY(gps['lon'],gps['lat'])
		gps_coords_ft = QgsFeature()
		gps_coords_ft.setGeometry(QgsGeometry.fromPointXY(point))
		gps_coords_ft.setAttributes([gps['cluster'], gps['type'], gps['lon'], gps['lat']])
		gps_coords_prov.addFeatures([gps_coords_ft])

	unique_clusters = set(val['cluster'] for val in gps_coords)
	unique_clusters_with_type = []
	for unique_cluster in unique_clusters:
		cluster_type = sorted([val['type'] for val in gps_coords if val['cluster'] == unique_cluster])[0]
		unique_clusters_with_type.append(tuple((unique_cluster, cluster_type)))

	for cl in unique_clusters_with_type:
		gps_coords_per_cluster = [val for val in gps_coords if val['cluster'] == cl[0]]
		gps_coords_list = []
		counter = 0
		for p in gps_coords_per_cluster:
			point = QgsPointXY(p['lon'],p['lat'])
			gps_coords_list.append(point)
			counter = counter + 1
		cluster_multipt_ft = QgsFeature()
		cluster_multipt_ft.setGeometry(QgsGeometry.fromMultiPointXY(gps_coords_list))
		cluster_multipt_ft.setAttributes([cl[0], cl[1], counter])
		cluster_multipt_prov.addFeatures([cluster_multipt_ft])

		cluster_convexhull_ft = QgsFeature()
		cluster_convexhull_ft.setGeometry(QgsGeometry.fromPolygonXY([gps_coords_list]).convexHull())

		# calculate convex hull geometry params
		cluster_convexhull_geom_merc = QgsGeometry(cluster_convexhull_ft.geometry())
		cluster_convexhull_geom_merc.transform(tr)
		cluster_convexhull_mbb = cluster_convexhull_geom_merc.orientedMinimumBoundingBox()

		area_m2 = cluster_convexhull_mbb[1]
		angle_deg = cluster_convexhull_mbb[2]
		width_m = cluster_convexhull_mbb[3]
		height_m = cluster_convexhull_mbb[4]
		if area_m2 == 1.7976931348623157e+308: area_m2 = 0 # handling infinity values
		if angle_deg == 1.7976931348623157e+308: angle_deg = 0 # handling infinity values
		if width_m == 1.7976931348623157e+308: width_m = 0 # handling infinity values
		if height_m == 1.7976931348623157e+308: height_m = 0 # handling infinity values

		cluster_convexhull_ft.setAttributes([cl[0], cl[1], counter, area_m2, angle_deg, width_m, height_m])
		cluster_convexhull_prov.addFeatures([cluster_convexhull_ft])

		cluster_centroid_ft = QgsFeature()

		# determine if pole of inaccessibility can be determined
		if cluster_convexhull_ft.geometry().poleOfInaccessibility(100)[0].isNull():
			cluster_centroid_ft.setGeometry(cluster_multipt_ft.geometry().centroid())
		else:
			cluster_centroid_ft.setGeometry(cluster_convexhull_ft.geometry().poleOfInaccessibility(100)[0])
		cluster_centroid_ft.setAttributes([cl[0], cl[1], counter])
		cluster_centroid_prov.addFeatures([cluster_centroid_ft])

		# cluster_centroid_fts.append(cluster_centroid_ft)

elif input_file_clusters_format == "shp":
	if cluster_lyr.wkbType() == 1: #QgsWkbTypes.Point
		cluster_centroids = [ft for ft in cluster_lyr.getFeatures()]
		for cluster_centroid in cluster_centroids:
			cluster_centroid_ft = QgsFeature()
			cluster_centroid_ft.setAttributes([cluster_centroid[cluster_no_field], cluster_centroid[cluster_type_field], 1])
			cluster_centroid_ft.setGeometry(cluster_centroid.geometry())
			cluster_centroid_prov.addFeatures([cluster_centroid_ft])

	if cluster_lyr.wkbType() == 6: #QgsWkbTypes.Polygon
		cluster_polygons = [ft for ft in cluster_lyr.getFeatures()]
		for cluster_polygon in cluster_polygons:
			cluster_centroid_ft = QgsFeature()
			cluster_centroid_ft.setAttributes([cluster_polygon[cluster_no_field], cluster_polygon[cluster_type_field], 1])
			cluster_centroid_ft.setGeometry(cluster_polygon.geometry().poleOfInaccessibility(100)[0])
			cluster_centroid_prov.addFeatures([cluster_centroid_ft])
			# cluster_centroid_fts.append(cluster_centroid_ft)

for cluster_centroid_ft in cluster_centroid_lyr.getFeatures():
	# copy geometry of centroid
	cluster_centroid_ft_geom_merc = QgsGeometry(cluster_centroid_ft.geometry())
	# transform copy of the centroid into Web Mercator
	cluster_centroid_ft_geom_merc.transform(tr)
	# cluster_centroid_ft_geom_merc

	# cluster centroid coordinates in Web Mercator
	x = cluster_centroid_ft_geom_merc.asPoint().x()
	y = cluster_centroid_ft_geom_merc.asPoint().y()

	# get subnational ID for the cluster
	subnational_ids = ref_fts_index.intersects(cluster_centroid_ft.geometry().boundingBox())
	intersecting_fts = []
	for s in subnational_ids:
		ft = ref_lyr.getFeature(s)
		if ft.geometry().intersects(cluster_centroid_ft.geometry()):
			intersecting_fts.append(ft)
	if len(intersecting_fts) == 0:
		ref_id_before = 'None'
	elif len(intersecting_fts) == 1:
		ref_ft_before = intersecting_fts[0]
		ref_id_before = getval(ref_ft_before, ref_id_field)
	else:
		ref_id_before = 'Many'

	cluster_type = cluster_centroid_ft[1]
	# define max distance depending on cluster type
	if cluster_type in urban_types:
		max_displace_distance = 2000
	elif cluster_type in rural_types:
		rural_displaced_points += 1
		max_displace_distance = (rural_displaced_points % 100 == 0) and 10000 or 5000
	else:
		max_displace_distance = 5000

	con = True
	iterations = 0
	while con:
		# call displacement function
		new_x, new_y, distance, angle_degree = displacepoint(x, y, max_displace_distance)

		# create geometry of a displaced centroid in Web Mercator
		displaced_point_mercator = QgsPointXY(new_x, new_y)

		# define reverse transformation
		tr_back = QgsCoordinateTransform(destCrs, sourceCrs, QgsProject.instance())

		# copy geometry of a displaced centroid
		displaced_point_wgs = QgsGeometry.fromPointXY(displaced_point_mercator)

		# transform copy of geometry of a displaced centroid into WGS84
		displaced_point_wgs.transform(tr_back)
		# displaced_point_wgs

		# get subnational ID for the cluster
		subnational_ids_after = ref_fts_index.intersects(displaced_point_wgs.boundingBox())
		intersecting_fts_after = []
		for s in subnational_ids_after:
			ft = ref_lyr.getFeature(s)
			if ft.geometry().intersects(displaced_point_wgs):
				intersecting_fts_after.append(ft)
		if len(intersecting_fts_after) == 0:
			ref_id_after = 'None'
		elif len(intersecting_fts_after) == 1:
			ref_ft_after = intersecting_fts_after[0]
			ref_id_after = getval(ref_ft_after, ref_id_field)
		else:
			ref_id_after = 'Many'

		if ref_id_after == ref_id_before: con = False
		iterations += 1
		print("Cluster: {}, ref_id_before: {}, ref_id_after: {}, iteration: {}". format(cluster_centroid_ft['cluster'], ref_id_before, ref_id_after, iterations))
		if iterations > 10: con = False

	# add displaced centroid
	feat_disp_centroid = QgsFeature()
	feat_disp_centroid.setGeometry(displaced_point_wgs)
	feat_disp_centroid.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], cluster_centroid_ft['count'], cluster_centroid_ft.geometry().asPoint().x(), cluster_centroid_ft.geometry().asPoint().y(), displaced_point_wgs.asPoint().x(), displaced_point_wgs.asPoint().y(), distance, angle_degree, ref_id_before, ref_id_after, iterations])
	cluster_disp_centroid_prov.addFeatures([feat_disp_centroid])

	# add anoymized displaced centroid
	feat_anonym_disp_centroid = QgsFeature()
	feat_anonym_disp_centroid.setGeometry(displaced_point_wgs)
	feat_anonym_disp_centroid.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], displaced_point_wgs.asPoint().x(), displaced_point_wgs.asPoint().y()])
	cluster_anonym_disp_centroid_prov.addFeatures([feat_anonym_disp_centroid])

	# add displacement links
	centroid_disp_links_ft = QgsFeature()
	centroid_disp_links_ft.setGeometry(QgsGeometry.fromPolylineXY([cluster_centroid_ft.geometry().asPoint(), feat_disp_centroid.geometry().asPoint()]))
	centroid_disp_links_ft.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], cluster_centroid_ft['count'], cluster_centroid_ft.geometry().asPoint().x(), cluster_centroid_ft.geometry().asPoint().y(), displaced_point_wgs.asPoint().x(), displaced_point_wgs.asPoint().y(), distance, angle_degree, ref_id_before, ref_id_after, iterations])
	cluster_centroid_disp_links_prov.addFeatures([centroid_disp_links_ft])

	# copy geometry of displaced centroid
	displaced_feat_centroid_mercator = QgsGeometry(feat_disp_centroid.geometry())
	# transform copy of the centroid into Web Mercator
	displaced_feat_centroid_mercator.transform(tr)

	# create buffers around displaced centroids
	disp_centroid_buff_geom = displaced_feat_centroid_mercator.buffer(max_displace_distance, 20)
	disp_centroid_buff_geom.transform(tr_back)
	disp_centroid_buff_ft = QgsFeature()
	disp_centroid_buff_ft.setGeometry(disp_centroid_buff_geom)
	disp_centroid_buff_ft.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], cluster_centroid_ft['count'], max_displace_distance])
	cluster_disp_centroid_buffer_prov.addFeatures([disp_centroid_buff_ft])

	# create buffers around displaced centroids
	disp_anonym_centroid_buff_ft = QgsFeature()
	disp_anonym_centroid_buff_ft.setGeometry(disp_centroid_buff_geom)
	disp_anonym_centroid_buff_ft.setAttributes([cluster_centroid_ft['cluster'], cluster_centroid_ft['type'], max_displace_distance])
	cluster_anonym_disp_centroid_buffer_prov.addFeatures([disp_anonym_centroid_buff_ft])

	# create buffers around original centroids
	# centroid_buff = cluster_centroid_ft_geom_merc.buffer(max_displace_distance, 20)
	# centroid_buff.transform(tr_back)
	# feat_centroid_buff = QgsFeature()
	# feat_centroid_buff.setGeometry(centroid_buff)
	# feat_centroid_buff.setAttributes([cl[0], cl[1], counter, max_displace_distance])
	# cluster_disp_centroid_buffer_prov.addFeatures([feat_centroid_buff])

# update extent and add relevant layers
registry = QgsProject.instance()

if input_file_clusters_format == "csv":
	# Update extent of the layer and add to map
	cluster_convexhull_lyr.updateExtents()
	registry.addMapLayer(cluster_convexhull_lyr)

	gps_coords_lyr.updateExtents()
	registry.addMapLayer(gps_coords_lyr)

	cluster_multipt_lyr.updateExtents()
	registry.addMapLayer(cluster_multipt_lyr)

if input_file_clusters_format == "shp":
	cluster_lyr.updateExtents()
	registry.addMapLayer(cluster_lyr)

# Update extent of the layer and add to map
cluster_disp_centroid_buffer_lyr.updateExtents()
registry.addMapLayer(cluster_disp_centroid_buffer_lyr)

cluster_anonym_disp_centroid_buffer_lyr.updateExtents()
registry.addMapLayer(cluster_anonym_disp_centroid_buffer_lyr)

cluster_centroid_disp_links_lyr.updateExtents()
registry.addMapLayer(cluster_centroid_disp_links_lyr)

cluster_centroid_lyr.updateExtents()
registry.addMapLayer(cluster_centroid_lyr)

cluster_disp_centroid_lyr.updateExtents()
registry.addMapLayer(cluster_disp_centroid_lyr)

cluster_anonym_disp_centroid_lyr.updateExtents()
registry.addMapLayer(cluster_anonym_disp_centroid_lyr)

print("Successfully completed at {}".format(datetime.now()))