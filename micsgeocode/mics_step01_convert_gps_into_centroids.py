from . import Step01Manager as Step01Manager

from . import mics_step01_inputs as Inputs


# UNTESTED


####################################################################
# 1st way - Using facade
####################################################################

manager = Step01Manager.Step01Manager()

manager.setReferenceLayer(Inputs.ref_lyr_name)
manager.setReferenceLayerField(Inputs.ref_id_field))
manager.setCentroidFile(Inputs.input_file_clusters)
manager.setLatField(Inputs.lat_field)
manager.setLongField(Inputs.lon_field)
manager.setClusterNoField(Inputs.cluster_no_field)
manager.setClusterTypeField(Inputs.cluster_type_field)
manager.setUrbanTypes(Inputs.urban_types)
manager.setRuralTypes(Inputs.rural_types)

manager.loadCentroids()

manager.displaceCentroids()

####################################################################
# 2nd way - Using High level object
####################################################################

from . import CentroidsLoader as Loader
from . import CentroidsDisplacer as Displacer

# Load Centroids

loader=Loader.CentroidsLoader()

loader.input_file=Inputs.input_file_clusters
loader.lon_field=Inputs.lon_field
loader.lat_field=Inputs.lat_field
loader.cluster_no_field=Inputs.cluster_no_field
loader.cluster_type_field=Inputs.cluster_type_field

centroid_layer=loader.loadCentroids()

# Displace Centroids

displacer=Displacer.CentroidsDisplacer()

displacer.layers[Utils.LayersName.CENTROIDS]=centroid_layer
displacer.lon_field=Inputs.lon_field
displacer.lat_field=Inputs.lat_field
displacer.cluster_no_field=Inputs.cluster_no_field
displacer.cluster_type_field=Inputs.cluster_type_field
displacer.ref_id_field=Inputs.ref_id_field


displacer.displaceCentroids()
