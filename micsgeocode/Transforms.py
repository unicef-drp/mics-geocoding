## ###########################################################################
##
## Transforms.py
##
## Author: Etienne Delclaux
## Created: 17/03/2021 11:15:56 2016 (+0200)
##
## Description:
##
## ###########################################################################

from qgis.core import *

class Transforms():
    """ Holds the transformations ofr the plugin
		Acts asa static class, with static attributes
        It is helpful to encapsulate the values of this transformations
    """
    proj4_4326 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
    # sourceCrs = QgsCoordinateReferenceSystem("EPSG:4326")
    sourceCrs = QgsCoordinateReferenceSystem("PROJ4:"+proj4_4326)
    destCrs = QgsCoordinateReferenceSystem("EPSG:3857")
    tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
    tr_back = QgsCoordinateTransform(destCrs, sourceCrs, QgsProject.instance())

    # layer_proj="epsg:4326"
    layer_proj="PROJ4:"+proj4_4326