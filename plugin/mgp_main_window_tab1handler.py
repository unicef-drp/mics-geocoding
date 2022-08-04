## ###########################################################################
##
# mgp_main_widow.py
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
from datetime import datetime

import re
import typing

from .ui_mgp_dialog import Ui_MGPDialog
from .micsgeocode import CentroidsLoader as Loader
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3


class MGPMainWindowTab1Handler(QtCore.QObject):
    '''The actual window that is displayed in the qgis interface
    '''
    # Define a signal called 'centroidsLoaded'
    centroidsLoaded = QtCore.pyqtSignal()

    def __init__(self, ui):
        """Interface initialisation : display interface and define events"""
        super().__init__()

        self.ui = ui
        self.needsSave = False

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.centroidsSourceFileToolButton.clicked.connect(self.onCentroidsSourceFileToolButtonClicked)
        self.ui.centroidsSourceFileLineEdit.textChanged.connect(self.onCentroidsSourceFileChanged)

        self.ui.longitudeFieldComboBox.currentTextChanged.connect(self.onLongitudeFieldChanged)
        self.ui.latitudeFieldComboBox.currentTextChanged.connect(self.onLatitudeFieldChanged)
        self.ui.numeroFieldComboBox.currentTextChanged.connect(self.onNumeroFieldChanged)
        self.ui.typeFieldComboBox.currentTextChanged.connect(self.onTypeFieldChanged)
        self.ui.adminBoundariesFieldComboBox.currentTextChanged.connect(self.onAdminBoundariesFieldChanged)

        self.ui.loadCentroidsButton.clicked.connect(self.onLoadCentroidsButtonCLicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.centroidsSourceFileToolButton.setToolTip("Browse for source file on the computer. Must be CSV file or shapefile (polygon or point layer).")
        self.ui.centroidsSourceFileLineEdit.setToolTip("Cluster source file on the computer.")

        self.ui.numeroFieldComboBox.setToolTip("Choose the field indicating cluster number variable.")
        self.ui.typeFieldComboBox.setToolTip("Choose the field indicating cluster area variable.")
        self.ui.longitudeFieldComboBox.setToolTip("Choose the field indicating longitude. Must be in decimal degree.")
        self.ui.latitudeFieldComboBox.setToolTip("Choose the field indicating latitude. Must be in decimal degree.")
        self.ui.adminBoundariesFieldComboBox.setToolTip("Administrative boundaries. Choose the field indicating administrative boundaries variable of displacement level.")

        self.ui.loadCentroidsButton.setToolTip("Generate Centroids. QGIS generates layers depending on input.")

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
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
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
        self.ui.adminBoundariesFieldComboBox.clear()

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

        # init cluster combobox and look for a default value
        self.ui.adminBoundariesFieldComboBox.addItems(fields)
        candidates = ["adminBoundaries", "AdminBoundaries", "ADMINBOUNDARIES", "region", "Region", "REGION"]
        for item in candidates:
            if item in fields:
                self.ui.adminBoundariesFieldComboBox.setCurrentIndex(fields.index(item))
                break

    def onLongitudeFieldChanged(self) -> typing.NoReturn:
        '''Update longitude field
        '''
        self.updateSaveStatus(True)

    def onLatitudeFieldChanged(self) -> typing.NoReturn:
        '''Update latitude field
        '''
        self.updateSaveStatus(True)

    def onNumeroFieldChanged(self) -> typing.NoReturn:
        '''Update numero field
        '''
        self.updateSaveStatus(True)

    def onTypeFieldChanged(self) -> typing.NoReturn:
        '''Update type field
        '''
        self.updateSaveStatus(True)

    def onAdminBoundariesFieldChanged(self) -> typing.NoReturn:
        '''Update longitude field
        '''
        self.updateSaveStatus(True)

    ## #############################################################
    # Main actions
    ## #############################################################

    def onLoadCentroidsButtonCLicked(self) -> typing.NoReturn:
        '''Load centroids
        '''
        if not self.ui.centroidsSourceFileLineEdit.text():
            Logger.logWarning("[CentroidsLoader] A valid centroid source file must be provided")
            return
        else:
            if self.ui.longitudeFieldComboBox.isEnabled() and not self.ui.longitudeFieldComboBox.currentText():
                Logger.logWarning("[CentroidsLoader] A valid longitude field must be provided")
                return

            if self.ui.latitudeFieldComboBox.isEnabled() and not self.ui.latitudeFieldComboBox.currentText():
                Logger.logWarning("[CentroidsLoader] A valid latitude field must be provided")
                return

            if self.ui.numeroFieldComboBox.isEnabled() and not self.ui.numeroFieldComboBox.currentText():
                Logger.logWarning("[CentroidsLoader] A valid numero field must be provided")
                return

            if self.ui.typeFieldComboBox.isEnabled() and not self.ui.typeFieldComboBox.currentText():
                Logger.logWarning("[CentroidsLoader] A valid latitude field must be provided")
                return

            if self.ui.adminBoundariesFieldComboBox.isEnabled() and not self.ui.adminBoundariesFieldComboBox.currentText():
                Logger.logWarning("[CentroidsLoader] A valid admin boundaries field must be provided")
                return

            Logger.logWarning("[CentroidsLoader] A problem occured while loading centroids")

        try:
            loader = Loader.CentroidsLoader()

            loader.input_file = self.ui.centroidsSourceFileLineEdit.text()

            loader.lon_field = self.ui.longitudeFieldComboBox.currentText()
            loader.lat_field = self.ui.latitudeFieldComboBox.currentText()
            loader.cluster_no_field = self.ui.numeroFieldComboBox.currentText()
            loader.cluster_type_field = self.ui.typeFieldComboBox.currentText()
            loader.admin_boundaries_field = self.ui.adminBoundariesFieldComboBox.currentText()

            loader.loadCentroids()
            Logger.logSuccess("[CentroidsLoader] Centroids succcessfully loaded at {}".format(datetime.now()))

            self.centroidsLoaded.emit()
        except:
            Logger.logWarning("[CentroidsLoader] A problem occured while loading centroids")
