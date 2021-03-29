## ###########################################################################
##
# Step01Manager.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

from qgis.core import *  # QGIS3

import os
from .Logger import Logger
import qgis.utils

from . import Utils

class ReferenceLayer():
    """ Facade that handle ReferenceLayerManagement.
    """
    def __init__(self):
        self.layer = None
        self.__layerName = ""
        self.ref_fts_index = None

    def clear(self):
        Utils.removeLayerIfExists(self.__layerName)
        self.__layerName = ""
        self.layer = None

    def load(self, input_file: str) -> QgsVectorLayer:
        """ Is in a specific folder.
            set inputs, call loader and displace with proper arguments.
        """
        self.clear()
        try:
            self.__layerName = os.path.basename(input_file)
            self.layer = QgsVectorLayer(input_file, self.__layerName)
            QgsProject.instance().addMapLayer(self.layer)
            self.ref_fts_index = QgsSpatialIndex(self.layer.getFeatures())
            # qgis.utils.iface.mapCanvas().setExtent(self.layer.extent())
        except:
            self.clear()
