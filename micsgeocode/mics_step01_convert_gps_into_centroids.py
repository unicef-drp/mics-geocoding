## ###########################################################################
##
# demo, untested
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################


from . import Step01Manager as Step01Manager

######################################
# CONFIG FOR SAMPLE 01
######################################
input_file_clusters = r'C:\Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample01\sample01_cluster_centroids.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
# column name with latitude (WGS84) coordinate (must be double, not string)
lat_field = 'Lat'
# column name with longitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'

# values form the cluster type column that belong to urban type
urban_types = ['U']
# values form the cluster type column that belong to rural type
rural_types = ['R']


# name of the QGIS layer with admin boundaries
ref_lyr_name = r'C: \Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample01\ago_admin2.shp'
# column name with a unique ID (e.g. pcode) for admin unit
ref_id_field = 'GID_2'

######################################
# CONFIG FOR SAMPLE 02
######################################
input_file_clusters = r'C:\Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample02\sample02_cluster_polygons.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
# column name with latitude (WGS84) coordinate (must be double, not string)
lat_field = 'Lat'
# column name with longitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'

# values form the cluster type column that belong to urban type
urban_types = ['U']
# values form the cluster type column that belong to rural type
rural_types = ['R']

ref_lyr_name = r'C: \Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample02\ago_admin2.shp'
# column name with a unique ID (e.g. pcode) for admin unit
ref_id_field = 'GID_2'


######################################
# CONFIG FOR SAMPLE 03
######################################
input_file_clusters = r'C:\Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample03\sample03_cluster_centroids_table.csv'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
# column name with latitude (WGS84) coordinate (must be double, not string)
lat_field = 'Lat'
# column name with longitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'

# values form the cluster type column that belong to urban type
urban_types = ['U']
# values form the cluster type column that belong to rural type
rural_types = ['R']

ref_lyr_name = r'C: \Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample03\ago_admin2.shp'
# column name with a unique ID (e.g. pcode) for admin unit
ref_id_field = 'GID_2'


######################################
# CONFIG FOR SAMPLE 04
######################################
input_file_clusters = r'C:\Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample04\sample04_cluster_coordinates_pt.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
# column name with latitude (WGS84) coordinate (must be double, not string)
lat_field = 'Lat'
# column name with longitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'

# values form the cluster type column that belong to urban type
urban_types = ['U']
# values form the cluster type column that belong to rural type
rural_types = ['R']

ref_lyr_name = r'C: \Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample04\ago_admin2.shp'
# column name with a unique ID (e.g. pcode) for admin unit
ref_id_field = 'GID_2'


######################################
# CONFIG FOR SAMPLE 05
######################################
input_file_clusters = r'C:\Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample05\sample05_cluster_polygons.shp'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
# column name with latitude (WGS84) coordinate (must be double, not string)
lat_field = 'Lat'
# column name with longitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'

# values form the cluster type column that belong to urban type
urban_types = ['U']
# values form the cluster type column that belong to rural type
rural_types = ['R']

ref_lyr_name = r'C: \Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample05\fji_admin1.shp'
# column name with a unique ID (e.g. pcode) for admin unit
ref_id_field = 'GID_1'


######################################
# CONFIG FOR SAMPLE 06
######################################
input_file_clusters = r'C:\Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample06\sample06_cluster_coordinates_tab.csv'
cluster_no_field = 'ClusterNo'
cluster_type_field = 'Type'
# column name with latitude (WGS84) coordinate (must be double, not string)
lat_field = 'Lat'
# column name with longitude (WGS84) coordinate (must be double, not string)
lon_field = 'Lon'

# values form the cluster type column that belong to urban type
urban_types = ['U']
# values form the cluster type column that belong to rural type
rural_types = ['R']

ref_lyr_name = r'C: \Users\Etienne\Documents\devel\mics-geocode-dataset\\Sample06\ago_admin2.shp'
# column name with a unique ID (e.g. pcode) for admin unit
ref_id_field = 'GID_2'


# UNTESTED


####################################################################
# 1st way - Using facade
####################################################################

manager = Step01Manager.Step01Manager()

manager.setReferenceLayer(ref_lyr_name)
manager.setReferenceLayerField(ref_id_field))
manager.setCentroidFile(input_file_clusters)
manager.setLatField(lat_field)
manager.setLongField(lon_field)
manager.setClusterNoField(cluster_no_field)
manager.setClusterTypeField(cluster_type_field)
manager.setUrbanTypes(urban_types)
manager.setRuralTypes(rural_types)

manager.loadCentroids()

manager.displaceCentroids()

####################################################################
# 2nd way - Using High level object
####################################################################

from . import CentroidsLoader as Loader
from . import CentroidsDisplacer as Displacer

# Load Centroids

loader=Loader.CentroidsLoader()

loader.input_file = input_file_clusters
loader.lon_field = lon_field
loader.lat_field = lat_field
loader.cluster_no_field = cluster_no_field
loader.cluster_type_field = cluster_type_field

centroid_layer=loader.loadCentroids()

# Displace Centroids

displacer=Displacer.CentroidsDisplacer()

displacer.setCentroidsLayer(centroid_layer)
displacer.lon_field = lon_field
displacer.lat_field = lat_field
displacer.cluster_no_field = cluster_no_field
displacer.cluster_type_field = cluster_type_field
displacer.ref_id_field = ref_id_field

displacer.displaceCentroids()
