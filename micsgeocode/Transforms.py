## ###########################################################################
##
# Transforms.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
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

    # web mercator, keeps angle, but not distance
    # the difference is computed by qgis, ans is OK. 5km at ecuador and 500m at the poles.
    # this is not really an issue -> the computation are good.
    destCrs = QgsCoordinateReferenceSystem("EPSG:3857")

    # voir avec Carto ? -> Benjamin, Gilles, Stephane.

    # projection sphérique ?
    # destCrs = QgsCoordinateReferenceSystem("EPSG:3857")

    # projection ECEF ? 4978 ? Nope
    # destCrs = QgsCoordinateReferenceSystem("EPSG:4978")

    # projection Custom ?
    # destCrs = QgsCoordinateReferenceSystem("PROJ4:"+proj4_custom)
    # proj4_custom = "+proj=ortho +lat_0=13.5 +lon_0=121.9 +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs"

    # projection UTM locale ?

    # xxxx, keeps surface, but not angle

    # Current projection --> Nope
    # Solution: change of projection

    tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
    tr_back = QgsCoordinateTransform(destCrs, sourceCrs, QgsProject.instance())

    # layer_proj="epsg:4326"
    layer_proj = "PROJ4:"+proj4_4326


# def computeEPSGCode(self, longitude, latitude):
#     zone = 0
#     if (latitude == 72) and (latitude <= 84):
#         zone = 32
#     elif (latitude >= 56) and (latitude < 64) and (longitude >= 3) and (longitude < 12):
#         zone = 32
#     elif (latitude >= 72) and (latitude < 84):
#         if (latitude >= 0) and (latitude < 9):
#             zone = 31
#         elif (longitude >= 9) and (longitude < 21):
#             zone = 33
#         elif (longitude >= 21) and (longitude < 33):
#             zone = 35
#         elif (longitude >= 33) and (longitude < 42):
#             zone = 37
#     else:
#         zone = math.floor((longitude + 180)/6) + 1

#     if (latitude > 0):
#         return int(32600 + zone)
#     else:
#         return int(32700 + zone)
