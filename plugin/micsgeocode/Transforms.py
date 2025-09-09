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
from math import floor

class CRS():
    """ 
        Holds the CRS definitions.
        Acts asa static class, with static attributes.
    """
    proj4_4326 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
    layer_proj = "PROJ4:"+proj4_4326
    WGS84 = "PROJ4:"+proj4_4326

class Transforms():
    """ Holds the transformations for the plugin
        It is helpful to encapsulate the values of this transformations
    """

    def __init__(self, lat: float, lon: float):
        """ Constructor
        """
        #self.lat = lat
        #self.lon = lon

        # Define the source CRS as WGS 84 (EPSG:4326)
        #self.proj4_4326 = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
        #self.layer_proj = "PROJ4:"+self.proj4_4326
        self.sourceCrs = QgsCoordinateReferenceSystem(CRS.WGS84)
        
        # Define the destination CRS
        self.destEPSG = str(get_epsg_code(lon, lat))
        self.destCrs = QgsCoordinateReferenceSystem(f"EPSG:{self.destEPSG}")

        # Define the transformations
        self.tr = QgsCoordinateTransform(self.sourceCrs, self.destCrs, QgsProject.instance())
        self.tr_back = QgsCoordinateTransform(self.destCrs, self.sourceCrs, QgsProject.instance())

def get_utm_zone_info(longitude: float, latitude: float) -> tuple:
    """
    Returns a dictionary with the UTM zone (e.g. '33U'), the zone number, and the hemisphere ('N' or 'S').
    Considers the exceptions for Norway and Svalbard.
    """
    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 y 180 degrees.")
    if not -80 <= latitude <= 84:
        raise ValueError("Latitude must be between -80 y 84 degrees.")

    # Initial zone calculation
    zone_number = floor((longitude + 180) / 6) + 1
    hemisphere = 'N' if latitude >= 0 else 'S'

    # Exception for Norway
    if (56.0 <= latitude < 64.0) and (3.0 <= longitude < 12.0):
        zone_number = 32

    # Exceptions for Svalbard
    if (72.0 <= latitude <= 84.0):
        if   (0.0 <= longitude <  9.0):  zone_number = 31
        elif (9.0 <= longitude < 21.0):  zone_number = 33
        elif (21.0 <= longitude < 33.0): zone_number = 35
        elif (33.0 <= longitude < 42.0): zone_number = 37

    # Latitude band letters (omits I y O to avoid confusion with numbers)
    lat_band_letters = "CDEFGHJKLMNPQRSTUVWX"
    band_index = floor((latitude + 80) / 8)
    band_letter = lat_band_letters[band_index] if band_index < len(lat_band_letters) else ''
    #print(f"Zone number: {zone_number}, Band letter: {band_letter}, Hemisphere: {hemisphere}")
    #print(f"Band letter: {band_letter}")
    return {
        "utm_zone": f"{zone_number}{band_letter}",
        "zone_number": zone_number,
        "hemisphere": hemisphere
    }

def get_epsg_code(longitude: float, latitude: float) -> int:
    """
    Returns the EPSG code corresponding to the given coordinates.
    """
    utm_zone_info = get_utm_zone_info(longitude, latitude)
    return 32600 + utm_zone_info['zone_number'] if utm_zone_info['hemisphere'] == 'N' else 32700 + utm_zone_info['zone_number']
