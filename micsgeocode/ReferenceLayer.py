## ###########################################################################
##
# ReferenceLayer.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

from qgis.core import *  # QGIS3
from PyQt5 import QtCore  # QGIS3

import typing

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

    def clear(self) -> typing.NoReturn:
        Utils.removeLayerIfExistsByName(self.__layerName)
        self.__layerName = ""
        self.layer = None

    def load(self, input_file: str) -> QgsVectorLayer:
        """ Is in a specific folder.
            set inputs, call loader and displace with proper arguments.
        """
        self.clear()
        try:
            fi = QtCore.QFileInfo(input_file)
            self.__layerName = fi.baseName()

            layers = QgsProject.instance().mapLayersByName(self.__layerName)
            if not layers:
                self.layer = QgsVectorLayer(input_file, self.__layerName)
            else:
                self.layer = layers[0]
            QgsProject.instance().addMapLayer(self.layer)
            self.ref_fts_index = QgsSpatialIndex(self.layer.getFeatures())

        except:
            self.clear()
