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
        # Init various members - might be overriden with config
        ## ####################################################################

        self.displacer = Displacer.CentroidsDisplacer()

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

        self.ui.referenceLayerToolButton.setToolTip("Browse for the reference Layer on the disk")
        self.ui.referenceLayerLineEdit.setToolTip("Reference Layer on the disk")
        self.ui.referenceLayerFieldCombobox.setToolTip("Reference layer field")
        self.ui.ruralValuesLineEdit.setToolTip("Field description for rural values. It can receive multiple values, splitted by ';' or ',' or ' '")
        self.ui.urbanValuesLineEdit.setToolTip("Field description for urban values. It can receive multiple values, splitted by ';' or ',' or ' '")

        self.ui.loadCentroidsFromStep01.setToolTip("Import step1 outputs as inputs")
        self.ui.centroidsLayerToolButton.setToolTip("Browse for the centroids layer on the disk")
        self.ui.centroidsLayerLineEdit.setToolTip("Browse for the centroids layer on the disk")
        self.ui.centroidsLayerNumeroFieldComboBox.setToolTip("Choose the field corresponding to cluster numero")
        self.ui.centroidsLayerTypeFieldComboBox.setToolTip("Choose the field corresponding to cluster type")

        self.ui.displaceCentroidsButton.setToolTip("Proceed centroids displacement")

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

     # #############################################################
    # Centroids Layer
    # #############################################################

    def loadCentroidsFromStep01Clicked(self) -> typing.NoReturn:
        '''Browse for centroid file
        '''

    def onCentroidsLayerToolButtonClicked(self) -> typing.NoReturn:
        '''Browse for centroid file
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open centroids layer file", dir, "(*.shp)")
        if file:
            self.centroidsLayerFile = file
            self.ui.centroidsLayerLineEdit.setText(os.path.normpath(self.centroidsLayerFile))
            settings.setValue("last_file_directory", os.path.dirname(self.centroidsLayerFile))

    def onCentroidsLayerChanged(self) -> typing.NoReturn:
        '''Handle new centroid file
        '''
        # Update manager
        # Use te file , not the Qgis Layer
        self.displacer.centroidLayer = self.ui.centroidsLayerLineEdit.text()
        self.updateSaveStatus(True)

    def onCentroidsLayerNumeroFieldChanged(self) -> typing.NoReturn:
        '''Update numero field
        '''
        # self.loader.cluster_no_field = self.ui.centroidsLayerNumeroFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onCentroidsLayerTypeFieldChanged(self) -> typing.NoReturn:
        '''Update type field
        '''
        # self.loader.cluster_type_field = self.ui.centroidsLayerTypeFieldComboBox.currentText()
        self.updateSaveStatus(True)

    # #############################################################
    # Reference Layer
    # #############################################################

    def onReferenceLayerToolButtonClicked(self) -> typing.NoReturn:
        '''handle browse for reference layer clicked
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open reference layer", dir, "*.shp")
        if file:
            self.ui.referenceLayerLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onReferenceLayerFileChanged(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        self.displacer.setReferenceLayer(self.ui.referenceLayerLineEdit.text())
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
        self.displacer.ref_id_field = self.ui.referenceLayerFieldCombobox.currentText()
        self.updateSaveStatus(True)

    # #############################################################
    # Urban, Rural values
    # #############################################################

    def onUrbanValuesLineEditChanged(self) -> typing.NoReturn:
        '''handle urban values field changed
        '''
        # separator can be ';' or ',' or ' '. feel free to add other
        list = re.split(';|,| ', self.ui.urbanValuesLineEdit.text())
        self.displacer.urban_types = [x for x in list if x]
        self.updateSaveStatus(True)

    def onRuralValuesLineEditChanged(self) -> typing.NoReturn:
        '''handle rural values field changed
        '''
        # separator can be ';' or ',' or ' '. feel free to add other
        list = re.split(';|,| ', self.ui.ruralValuesLineEdit.text())
        self.displacer.rural_types = [x for x in list if x]
        self.updateSaveStatus(True)

    ## #############################################################
    # Main actions
    ## #############################################################

    def onDisplaceCentroidsButtonClicked(self) -> typing.NoReturn:
        '''Displace centroids
        '''
        # Force reference layer to be up to date. Displacer might have been reseted since last ref update
        # self.loader.putLayersOnTop()
        self.displacer.setCentroidsLayer(self.layerCentroidsLoaded)
        self.displacer.displaceCentroids()
