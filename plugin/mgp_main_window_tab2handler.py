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
from .micsgeocode import CentroidsDisplacer as Displacer
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3


class MGPMainWindowTab2Handler():
    '''The actual window that is displayed in the qgis interface
    '''

    def __init__(self, ui):
        """Interface initialisation : display interface and define events"""
        Logger.logInfo("Building the object")

        self.ui = ui
        self.needsSave = False

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.referenceLayerToolButton.clicked.connect(self.onReferenceLayerToolButtonClicked)
        self.ui.referenceLayerLineEdit.textChanged.connect(self.onReferenceLayerFileChanged)
        self.ui.referenceLayerFieldCombobox.currentTextChanged.connect(self.onReferenceLayerFieldComboboxTextChanged)
        self.ui.ruralValuesLineEdit.textChanged.connect(self.onRuralValuesLineEditChanged)
        self.ui.urbanValuesLineEdit.textChanged.connect(self.onUrbanValuesLineEditChanged)

        self.ui.loadCentroidsFromStep01.clicked.connect(self.loadCentroidsFromStep01Clicked)
        self.ui.centroidsLayerToolButton.clicked.connect(self.onCentroidsLayerToolButtonClicked)
        self.ui.centroidsLayerLineEdit.textChanged.connect(self.onCentroidsLayerChanged)
        self.ui.centroidsLayerNumeroFieldComboBox.currentTextChanged.connect(self.onCentroidsLayerNumeroFieldChanged)
        self.ui.centroidsLayerTypeFieldComboBox.currentTextChanged.connect(self.onCentroidsLayerTypeFieldChanged)

        self.ui.displaceCentroidsButton.clicked.connect(self.onDisplaceCentroidsButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.referenceLayerToolButton.setToolTip("Browse for the boundary shapefile selected for cluster displacement.")
        self.ui.referenceLayerLineEdit.setToolTip("Boundary Layer on the computer.")
        self.ui.referenceLayerFieldCombobox.setToolTip("Choose the field corresponding to the boundary layer field.")
        self.ui.ruralValuesLineEdit.setToolTip("Field description for rural values. It can receive multiple values, splitted by ';' or ',' or ' '")
        self.ui.urbanValuesLineEdit.setToolTip("Field description for urban values. It can receive multiple values, splitted by ';' or ',' or ' '")

        self.ui.loadCentroidsFromStep01.setToolTip("Import step1 outputs as inputs")
        self.ui.centroidsLayerToolButton.setToolTip("Browse for centroids layer on the computer. Must be point shapefile.")
        self.ui.centroidsLayerLineEdit.setToolTip("Cluster centroids file on the computer.")
        self.ui.centroidsLayerNumeroFieldComboBox.setToolTip("Choose the field indicating cluster number variable.")
        self.ui.centroidsLayerTypeFieldComboBox.setToolTip("Choose the field indicating cluster area variable.")

        self.ui.displaceCentroidsButton.setToolTip(
            "Displace Centroids. QGIS generates additional layers depending on inputs.\nThe final anonymised displaced cluster file is generated “BASENAME_cluster_anonymised_displaced_centroids”.")

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

    # #############################################################
    # Load centroids from step01
    # #############################################################

    def loadCentroidsFromStep01Clicked(self) -> typing.NoReturn:
        '''Browse for centroid file
        '''
        # Utils.self.layers[Utils.LayersType.CENTROIDS]
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

        self.updateSaveStatus(True)

    def onCentroidsLayerNumeroFieldChanged(self) -> typing.NoReturn:
        '''Update numero field
        '''
        self.updateSaveStatus(True)

    def onCentroidsLayerTypeFieldChanged(self) -> typing.NoReturn:
        '''Update type field
        '''
        self.updateSaveStatus(True)

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
        self.updateSaveStatus(True)

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
        self.updateSaveStatus(True)

    # #############################################################
    # Urban, Rural values
    # #############################################################

    def onUrbanValuesLineEditChanged(self) -> typing.NoReturn:
        '''handle urban values field changed
        '''
        self.updateSaveStatus(True)

    def onRuralValuesLineEditChanged(self) -> typing.NoReturn:
        '''handle rural values field changed
        '''
        self.updateSaveStatus(True)

    ## #############################################################
    # Main action
    ## #############################################################

    def onDisplaceCentroidsButtonClicked(self) -> typing.NoReturn:
        '''Displace centroids
        '''
        if not self.ui.centroidsLayerLineEdit.text():
            Logger.logWarning("[CentroidsDisplacer] A valid centroid source file must be provided")
            return

        if not self.ui.referenceLayerLineEdit.text():
            Logger.logWarning("[CentroidsDisplacer] A valid reference source file must be provided")
            return
        else:
            if not self.ui.ruralValuesLineEdit.text():
                Logger.logWarning("[CentroidsDisplacer] Rural value(s) must be provided")
                return

            if not self.ui.urbanValuesLineEdit.text():
                Logger.logWarning("[CentroidsDisplacer] Rural value(s) must be provided")
                return

        try:
            displacer = Displacer.CentroidsDisplacer()

            # Centroid Layer
            centroidsLayerName = Utils.LayersName.layerName(Utils.LayersType.CENTROIDS)
            Utils.removeLayerIfExistsByName(centroidsLayerName)
            displacer.centroidLayer = QgsVectorLayer(self.ui.centroidsLayerLineEdit.text(), centroidsLayerName)
            QgsProject.instance().addMapLayer(displacer.centroidLayer)

            displacer.setReferenceLayer(self.ui.referenceLayerLineEdit.text())

            displacer.ref_id_field = self.ui.referenceLayerFieldCombobox.currentText()

            # separator can be ';' or ',' or ' '. feel free to add other
            displacer.rural_types = [x for x in re.split(';|,| ', self.ui.ruralValuesLineEdit.text()) if x]
            displacer.urban_types = [x for x in re.split(';|,| ', self.ui.urbanValuesLineEdit.text()) if x]

            displacer.displaceCentroids()

            Utils.putLayerOnTopIfExists(Utils.LayersType.CENTROIDS)

            Logger.logSuccess("[CentroidsDisplacer] Centroids succcessfully displaced at {}".format(datetime.now()))
        except:
            Logger.logWarning("[CentroidsDisplacer] A problem occured while displacing centroids")
