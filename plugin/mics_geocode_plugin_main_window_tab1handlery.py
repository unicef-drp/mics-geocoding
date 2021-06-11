## ###########################################################################
##
# mics_geocode_plugin_main_widow.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################


import os

from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
import re
import typing

from .ui_mics_geocode_plugin_dialog import Ui_MicsGeocodePluginDialog
from .micsgeocode import CentroidsLoader as Loader
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3


class MicsGeocodePluginMainWindowTab1Handler():
    '''The actual window that is displayed in the qgis interface
    '''

    def __init__(self, ui):
        """Interface initialisation : display interface and define events"""
        self.ui = ui
        self.needsSave = False

        ## ####################################################################
        # Init various members - might be overriden with config
        ## ####################################################################

        self.loader = Loader.CentroidsLoader()

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.centroidsSourceFileToolButton.clicked.connect(self.onCentroidsSourceFileToolButtonClicked)
        self.ui.centroidsSourceFileLineEdit.textChanged.connect(self.onCentroidsSourceFileChanged)

        self.ui.longitudeFieldComboBox.currentTextChanged.connect(self.onLongitudeFieldChanged)
        self.ui.latitudeFieldComboBox.currentTextChanged.connect(self.onLatitudeFieldChanged)
        self.ui.numeroFieldComboBox.currentTextChanged.connect(self.onNumeroFieldChanged)
        self.ui.typeFieldComboBox.currentTextChanged.connect(self.onTypeFieldChanged)

        self.ui.loadCentroidsButton.clicked.connect(self.onLoadCentroidsButtonCLicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.centroidsSourceFileToolButton.setToolTip("Browse for the centroids layer on the disk")
        self.ui.centroidsSourceFileLineEdit.setToolTip("Browse for the centroids layer on the disk")

        self.ui.longitudeFieldComboBox.setToolTip("Choose the field corresponding to longitude")
        self.ui.latitudeFieldComboBox.setToolTip("Choose the field corresponding to latitude")
        self.ui.numeroFieldComboBox.setToolTip("Choose the field corresponding to cluster numero")
        self.ui.typeFieldComboBox.setToolTip("Choose the field corresponding to cluster type")

        self.ui.loadCentroidsButton.setToolTip("Load Centroids")

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

    # #############################################################
    # Centroids Source
    # #############################################################

    def onCentroidsSourceFileToolButtonClicked(self) -> typing.NoReturn:
        '''Browse for centroid file
        '''
        Logger.logInfo("Browsing")
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open centroids file", dir, "(*.csv *.shp)")
        if file:
            self.centroidsFile = file
            self.ui.centroidsSourceFileLineEdit.setText(os.path.normpath(self.centroidsFile))
            settings.setValue("last_file_directory", os.path.dirname(self.centroidsFile))

    def onCentroidsSourceFileChanged(self) -> typing.NoReturn:
        '''Handle new centroid file
        '''
        # Update manager
        self.loader.input_file = self.ui.centroidsSourceFileLineEdit.text()
        self.updateCentroidCombobox()
        self.updateSaveStatus(True)

    def updateCentroidCombobox(self):
        # Retrieve fieldlist and populate comboboxes
        fields = Utils.getFieldsListAsStrArray(self.ui.centroidsSourceFileLineEdit.text())

        extension = Path(self.ui.centroidsSourceFileLineEdit.text()).suffix[1:]
        self.ui.typeFieldComboBox.clear()
        self.ui.numeroFieldComboBox.clear()
        self.ui.longitudeFieldComboBox.clear()
        self.ui.latitudeFieldComboBox.clear()

        # init type combobox and look for a default value
        self.ui.typeFieldComboBox.addItems(fields)
        candidates = ["Type", "type", "TYPE"]
        for item in candidates:
            if item in fields:
                self.ui.typeFieldComboBox.setCurrentIndex(fields.index(item))
                break

        # init cluster combobox and look for a default value
        self.ui.numeroFieldComboBox.addItems(fields)
        candidates = ["clusterno", "ClusterNo", "CLUSTERNO"]
        for item in candidates:
            if item in fields:
                self.ui.numeroFieldComboBox.setCurrentIndex(fields.index(item))
                break

        # habdle csv vs shp
        if extension == "csv":
            self.ui.longitudeFieldComboBox.setEnabled(True)
            self.ui.latitudeFieldComboBox.setEnabled(True)

            self.ui.longitudeFieldComboBox.addItems(fields)
            self.ui.latitudeFieldComboBox.addItems(fields)

            candidates = ["lat", "Lat", "LAT", "lat.", "Lat.",
                          "LAT.", "latitude", "Latitude", "LATITUDE"]
            for item in candidates:
                if item in fields:
                    self.ui.latitudeFieldComboBox.setCurrentIndex(fields.index(item))
                    break

            candidates = ["lon", "Lon", "LON", "lon.", "Lon.", "LON.", "long", "Long",
                          "LONG", "long.", "Long.", "LONG.", "longitude", "Longitud", "LONGITUDE"]
            for item in candidates:
                if item in fields:
                    self.ui.longitudeFieldComboBox.setCurrentIndex(fields.index(item))
                    break
        else:
            self.ui.longitudeFieldComboBox.setEnabled(False)
            self.ui.latitudeFieldComboBox.setEnabled(False)

    def onLongitudeFieldChanged(self) -> typing.NoReturn:
        '''Update longitude field
        '''
        self.loader.lon_field = self.ui.longitudeFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onLatitudeFieldChanged(self) -> typing.NoReturn:
        '''Update latitude field
        '''
        self.loader.lat_field = self.ui.latitudeFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onNumeroFieldChanged(self) -> typing.NoReturn:
        '''Update numero field
        '''
        self.loader.cluster_no_field = self.ui.numeroFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onTypeFieldChanged(self) -> typing.NoReturn:
        '''Update type field
        '''
        self.loader.cluster_type_field = self.ui.typeFieldComboBox.currentText()
        self.updateSaveStatus(True)

    ## #############################################################
    # Main actions
    ## #############################################################

    def onLoadCentroidsButtonCLicked(self) -> typing.NoReturn:
        '''Load centroids
        '''
        self.onCentroidsSourceFileChanged()
        self.onLongitudeFieldChanged()
        self.onLatitudeFieldChanged()
        self.onNumeroFieldChanged()
        self.onTypeFieldChanged()
        self.layerCentroidsLoaded = self.loader.loadCentroids()
