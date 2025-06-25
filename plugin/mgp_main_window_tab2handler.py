## ###########################################################################
##
# mgp_main_widow.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Updated: Nazim Gashi
# Time: 06/05/2024 13:00:00
# Time: 08/01/2025 15:00:00 (lines 316 and 319 added) (updates done between in 312 and 315)
##
# Description:
##
## ###########################################################################


import os
import csv

from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
from datetime import datetime

import re
import typing

from .ui_mgp_mainwindow import Ui_MGPDialog
from .micsgeocode import CentroidsDisplacer as Displacer
from .micsgeocode import CentroidBuffersMaxDistanceComputer as Radier
from .micsgeocode import CentroidBuffersLayerWriter as BufferWriter
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3


class MGPMainWindowTab2Handler(QtCore.QObject):
    '''The actual window that is displayed in the qgis interface
    '''
    # Define a signal called 'centroidsLoaded'
    centroidsDisplaced = QtCore.pyqtSignal()

    def __init__(self, mainwindow):
        """Interface initialisation : display interface and define events"""
        super().__init__()
        self.mainwindow = mainwindow
        self.ui = self.mainwindow.ui

        # Values are stored after the centroids displacement
        # --> Used for generating buffer around original buffer
        self.maxDistancesPerBufferId = None

        ## #############################################################
        # Animation init
        ## #############################################################

        self.showMoreWidgetSizeAnimation = QtCore.QPropertyAnimation(self.ui.moreWidget, b"size")
        self.showMoreWidgetSizeAnimation.setDuration(250)
        self.showMoreWidgetSizeAnimation.setStartValue(QtCore.QSize(461, 0))
        self.showMoreWidgetSizeAnimation.setEndValue(QtCore.QSize(461, 100))
        self.showMoreWidgetSizeAnimation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self.showLessWidgetSizeAnimation = QtCore.QPropertyAnimation(self.ui.moreWidget, b"size")
        self.showLessWidgetSizeAnimation.setDuration(250)
        self.showLessWidgetSizeAnimation.setStartValue(QtCore.QSize(461, 100))
        self.showLessWidgetSizeAnimation.setEndValue(QtCore.QSize(461, 0))
        self.showLessWidgetSizeAnimation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self.showLessIcon = self.ui.toggleShowMoreButton.style().standardIcon(getattr(QtWidgets.QStyle, "SP_TitleBarShadeButton"))
        self.showMoreIcon = self.ui.toggleShowMoreButton.style().standardIcon(getattr(QtWidgets.QStyle, "SP_TitleBarUnshadeButton"))

        self.isMoreVisible = False
        self.ui.moreWidget.setProperty(b"size", QtCore.QSize(41, 0))

        self.ui.toggleShowMoreButton.setText("Show More")
        self.ui.toggleShowMoreButton.setIcon(self.showMoreIcon)

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.referenceLayerToolButton.clicked.connect(self.onReferenceLayerToolButtonClicked)
        self.ui.referenceLayerLineEdit.textChanged.connect(self.onReferenceLayerFileChanged)
        self.ui.referenceLayerFieldCombobox.currentTextChanged.connect(self.onReferenceLayerFieldComboboxTextChanged)

        self.ui.centroidsLayerToolButton.clicked.connect(self.onCentroidsLayerToolButtonClicked)
        self.ui.centroidsLayerLineEdit.textChanged.connect(self.onCentroidsLayerChanged)
        self.ui.centroidsLayerNumeroFieldComboBox.currentTextChanged.connect(self.onCentroidsLayerNumeroFieldChanged)
        self.ui.centroidsLayerTypeFieldComboBox.currentTextChanged.connect(self.onCentroidsLayerTypeFieldChanged)
        self.ui.centroidsLayerAdminFieldComboBox.currentTextChanged.connect(self.onCentroidsLayerAdminFieldChanged)

        self.ui.displaceCentroidsButton.clicked.connect(self.onDisplaceCentroidsButtonClicked)

        self.ui.exportDisplacedCentroidsButton.clicked.connect(self.onExportDisplacedCentroidsButtonClicked)

        # Command window
        self.ui.toggleShowMoreButton.clicked.connect(self.onToggleShowMoreButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.referenceLayerToolButton.setToolTip("Browse for the boundary shapefile selected for cluster displacement.")
        self.ui.referenceLayerLineEdit.setToolTip("Boundary Layer on the computer.")
        self.ui.referenceLayerFieldCombobox.setToolTip("Choose the field corresponding to the boundary layer field.")

        self.ui.centroidsLayerToolButton.setToolTip("Browse for centroids layer on the computer. Must be point shapefile.")
        self.ui.centroidsLayerLineEdit.setToolTip("Cluster centroids file on the computer.")
        self.ui.centroidsLayerNumeroFieldComboBox.setToolTip("Choose the field indicating cluster number variable.")
        self.ui.centroidsLayerTypeFieldComboBox.setToolTip("Choose the field indicating cluster area variable.")
        self.ui.centroidsLayerAdminFieldComboBox.setToolTip("Choose the field indicating cluster admin variable.")

        self.ui.displaceCentroidsButton.setToolTip(
            "Displace Centroids. QGIS generates additional layers depending on inputs.\nThe final anonymised displaced cluster file is generated “BASENAME_cluster_anonymised_displaced_centroids”."
        )

        self.ui.exportDisplacedCentroidsButton.setToolTip("Export anonymised displaced cluster centroids as a CSV file.")

    ## #############################################################
    # reset
    ## #############################################################

    def reset(self) -> typing.NoReturn:

        self.ui.centroidsLayerLineEdit.clear()
        self.ui.referenceLayerLineEdit.clear()

        self.maxDistancesPerBufferId = None

        # hide show more section
        self.isMoreVisible = False
        self.ui.moreWidget.setProperty(b"size", QtCore.QSize(451, 0))

        self.ui.toggleShowMoreButton.setText("Show More")
        self.ui.toggleShowMoreButton.setIcon(self.showMoreIcon)

    ## #############################################################
    # show hide the more section
    ## #############################################################

    def onToggleShowMoreButtonClicked(self) -> typing.NoReturn:
        if self.isMoreVisible:
            self.ui.toggleShowMoreButton.setText("Show More")
            self.ui.toggleShowMoreButton.setIcon(self.showMoreIcon)
            self.showLessWidgetSizeAnimation.start()
        else:
            self.ui.toggleShowMoreButton.setText("Show Less")
            self.ui.toggleShowMoreButton.setIcon(self.showLessIcon)
            self.showMoreWidgetSizeAnimation.start()

        self.isMoreVisible = not self.isMoreVisible

    # #############################################################
    # Load centroids from step01
    # #############################################################

    def loadCentroidsFromStep01(self) -> typing.NoReturn:
        '''Browse for centroid file
        '''
        file = Utils.LayersName.fileName(Utils.LayersType.CENTROIDS)
        layer = None
        layers = QgsProject.instance().mapLayersByName(Utils.LayersName.layerName(Utils.LayersType.CENTROIDS))
        if layers:
            layer = layers[0]
        self.ui.centroidsLayerLineEdit.setText(file)

    # #############################################################
    # Centroids Layer
    # #############################################################

    def onCentroidsLayerToolButtonClicked(self) -> typing.NoReturn:
        '''Browse for centroid file
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open centroids layer file", dir, "(*.shp)")
        if file:
            self.ui.centroidsLayerLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onCentroidsLayerChanged(self) -> typing.NoReturn:
        '''Handle new centroid file
        '''
        # Update manager
        # Use te file , not the Qgis Layer
        # Retrieve fieldlist and populate comboboxes
        fields = Utils.getFieldsListAsStrArray(self.ui.centroidsLayerLineEdit.text())
        self.ui.centroidsLayerTypeFieldComboBox.clear()
        self.ui.centroidsLayerNumeroFieldComboBox.clear()
        self.ui.centroidsLayerAdminFieldComboBox.clear()

        # init type combobox and look for a default value
        self.ui.centroidsLayerAdminFieldComboBox.addItems(fields)
        candidates = ["Admin", "admin", "ADMIN"]
        for item in candidates:
            if item in fields:
                self.ui.centroidsLayerAdminFieldComboBox.setCurrentIndex(fields.index(item))
                break

        # init type combobox and look for a default value
        self.ui.centroidsLayerTypeFieldComboBox.addItems(fields)
        candidates = ["Type", "type", "TYPE"]
        for item in candidates:
            if item in fields:
                self.ui.centroidsLayerTypeFieldComboBox.setCurrentIndex(fields.index(item))
                break

        # init cluster combobox and look for a default value
        self.ui.centroidsLayerNumeroFieldComboBox.addItems(fields)
        candidates = ["clusterno", "ClusterNo", "CLUSTERNO"]
        for item in candidates:
            if item in fields:
                self.ui.centroidsLayerNumeroFieldComboBox.setCurrentIndex(fields.index(item))
                break

        self.mainwindow.updateSaveStatus(True)

    def onCentroidsLayerNumeroFieldChanged(self) -> typing.NoReturn:
        '''Update numero field
        '''
        self.mainwindow.updateSaveStatus(True)

    def onCentroidsLayerTypeFieldChanged(self) -> typing.NoReturn:
        '''Update type field
        '''
        self.mainwindow.updateSaveStatus(True)

    def onCentroidsLayerAdminFieldChanged(self) -> typing.NoReturn:
        '''Update type field
        '''
        self.mainwindow.updateSaveStatus(True)

    # #############################################################
    # Reference Layer
    # #############################################################

    def onReferenceLayerToolButtonClicked(self) -> typing.NoReturn:
        '''handle browse for reference layer clicked
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, " Open reference layer", dir, "*.shp")
        if file:
            self.ui.referenceLayerLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onReferenceLayerFileChanged(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        self.ui.referenceLayerFieldCombobox.clear()
        self.updateReferenceLayerCombobox()
        self.mainwindow.updateSaveStatus(True)

    def updateReferenceLayerCombobox(self):
        # retrieve field and update combobox
        fields = Utils.getFieldsListAsStrArray(self.ui.referenceLayerLineEdit.text())
        if fields:
            self.ui.referenceLayerFieldCombobox.addItems(fields)
            self.ui.referenceLayerFieldCombobox.setEnabled(True)
            self.ui.referenceLayerFieldCombobox.setCurrentIndex(0)
        else:
            self.ui.referenceLayerFieldCombobox.setEnabled(False)

    def onReferenceLayerFieldComboboxTextChanged(self) -> typing.NoReturn:
        '''handle reference field changed
        '''
        self.mainwindow.updateSaveStatus(True)

    ## #############################################################
    # Main action
    ## #############################################################

    def onDisplaceCentroidsButtonClicked(self) -> typing.NoReturn:
        '''Displace centroids
        '''
        if not self.ui.centroidsLayerLineEdit.text():
            Logger.logWarning("[Displace] A valid centroid source file must be provided")
            return

        if not self.ui.referenceLayerLineEdit.text():
            Logger.logWarning("[Displace] A valid reference source file must be provided")
            return

        try:
            self.maxDistancesPerBufferId = None

            displacer = Displacer.CentroidsDisplacer()

            # Read the name of the centroid shapefile used for the displacement
            centroidShpPath = self.ui.centroidsLayerLineEdit.text()

            # Centroid Layer
            centroidsLayerName = Utils.LayersName.layerName(Utils.LayersType.CENTROIDS)
            # Remove the layer is if it already exists and load the new one
            Utils.removeLayerIfExistsByName(centroidsLayerName)
            displacer.centroidLayer = QgsVectorLayer(centroidShpPath, centroidsLayerName)
            QgsProject.instance().addMapLayer(displacer.centroidLayer)

            displacer.set_field_mappings(
                cluster_no_field=self.ui.centroidsLayerNumeroFieldComboBox.currentText(),
                cluster_type_field=self.ui.centroidsLayerTypeFieldComboBox.currentText(),
                cluster_admin_field=self.ui.centroidsLayerAdminFieldComboBox.currentText()
            )

            displacer.setReferenceLayer(self.ui.referenceLayerLineEdit.text())
            displacer.ref_id_field = self.ui.referenceLayerFieldCombobox.currentText()

            displacer.displaceCentroids()

            Utils.putLayerOnTopIfExists(Utils.LayersType.CENTROIDS)

            Utils.reloadLayerFromDiskToAvoidMemoryFlag(Utils.LayersType.CENTROIDS)

            Logger.logSuccess("[Displace] Centroids succcessfully displaced")

            self.maxDistancesPerBufferId = displacer.maxDistances

            self.centroidsDisplaced.emit()
        except BaseException as e:
            Logger.logException("[Displace] A problem occured while displacing centroids", e)

    def onExportDisplacedCentroidsButtonClicked(self) -> typing.NoReturn:
        '''Displace centroids
        '''
        try:
            layers = QgsProject.instance().mapLayersByName(Utils.LayersName.layerName(Utils.LayersType.DISPLACEDANON))
            if layers:
                layer = layers[0]
                filename = Utils.LayersName.fileName(Utils.LayersType.DISPLACEDANON, "csv")
                with open(filename, 'w', encoding="UTF8", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["HH1", "HH6", "Longitude", "Latitude", "MICSGEO"])
                    for ft in layer.getFeatures():
                        writer.writerow([
                            str(ft['HH1']),
                            ft['HH6'],
                            "{:.6f}".format(ft.geometry().asPoint().x()),
                            "{:.6f}".format(ft.geometry().asPoint().y()),
                            ft['MICSGEO']
                        ])
                
                Logger.logSuccess("[Displace] Centroids succcessfully exported as CSV")

        except BaseException as e:
            Logger.logException("[Displace] A problem occured while saving displaced anonymised centroids", e)
