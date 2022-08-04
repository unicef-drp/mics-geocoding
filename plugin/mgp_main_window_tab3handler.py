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
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3
from .micsgeocode import CovariatesProcesser as CovariatesProcesser


class MGPMainWindowTab3Handler(QtCore.QObject):
    '''The actual window that is displayed in the qgis interface
    '''

    def __init__(self, ui):
        """Interface initialisation : display interface and define events"""
        super().__init__()

        self.ui = ui
        self.needsSave = False

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.covinputsSourceFileToolButton.clicked.connect(self.onCovinputsSourceFileToolButtonClicked)
        self.ui.covinputsSourceFileLineEdit.textChanged.connect(self.onCovinputsSourceFileChanged)

        self.ui.imagesSourceFileToolButton.clicked.connect(self.onImagesSourceFileToolButtonClicked)
        self.ui.imagesSourceFileLineEdit.textChanged.connect(self.onImagesSourceFileChanged)

        self.ui.filenameFieldComboBox.currentTextChanged.connect(self.onFilenameFieldChanged)
        self.ui.fileformatFieldComboBox.currentTextChanged.connect(self.onFileformatFieldChanged)
        self.ui.sumstatFieldComboBox.currentTextChanged.connect(self.onSumstatFieldChanged)
        self.ui.columnnameFieldComboBox.currentTextChanged.connect(self.onColumnnameFieldChanged)

        self.ui.covrefLayerToolButton.clicked.connect(self.onCovrefLayerToolButtonClicked)
        self.ui.covrefLayerLineEdit.textChanged.connect(self.onCovrefLayerFileChanged)

        self.ui.computeCovariatesButton.clicked.connect(self.onComputeCovariatesButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.covinputsSourceFileToolButton.setToolTip("Browse for covariates input file on the computer. Must be CSV file.")
        self.ui.covinputsSourceFileLineEdit.setToolTip("Covariates input file on the computer.")

        self.ui.imagesSourceFileToolButton.setToolTip("Browse for covariates input folder on the computer. Must contain image files listed in the “Covariates Input File”.")
        self.ui.imagesSourceFileLineEdit.setToolTip("Covariates input folder on the computer.")

        self.ui.filenameFieldComboBox.setToolTip("Choose the field indicating file name variable.")
        self.ui.fileformatFieldComboBox.setToolTip("Choose the field indicating file format variable.")
        self.ui.sumstatFieldComboBox.setToolTip("Choose the field indicating summary statistics variable.")
        self.ui.columnnameFieldComboBox.setToolTip("Choose the field indicating variable name variable.")

        self.ui.covrefLayerToolButton.setToolTip("Browse for the anonymised cluster buffer shapefile on the computer. It was generated to phase of cluster displacement (Displace).")
        self.ui.covrefLayerLineEdit.setToolTip("Anonymised cluster buffer shapefile on the computer.")

        self.ui.computeCovariatesButton.setToolTip("Compute covariates. QGIS generates additional layers depending on inputs and a CSV file with the outputs.")

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

    ## #############################################################
    # Load covref from step2
    ## #############################################################

    def loadCovrefFromStep02(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        file = Utils.LayersName.fileName(Utils.LayersType.BUFFERSANON)
        layer = None
        layers = QgsProject.instance().mapLayersByName(Utils.LayersName.layerName(Utils.LayersType.BUFFERSANON))
        if layers:
            layer = layers[0]
        self.ui.covrefLayerLineEdit.setText(file)

    # #############################################################
    # Covinputs Source
    # #############################################################

    def onCovinputsSourceFileToolButtonClicked(self) -> typing.NoReturn:
        '''Browse for covinputs file
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open covinputs file", dir, "*.csv")
        if file:
            self.ui.covinputsSourceFileLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onCovinputsSourceFileChanged(self) -> typing.NoReturn:
        '''Handle new covinput file
        '''
        self.updateCovinputsComboBoxes()
        self.updateSaveStatus(True)

    def updateCovinputsComboBoxes(self):
        # Retrieve fieldlist and populate comboboxes
        fields = Utils.getFieldsListAsStrArray(self.ui.covinputsSourceFileLineEdit.text())

        self.ui.filenameFieldComboBox.clear()
        self.ui.fileformatFieldComboBox.clear()
        self.ui.sumstatFieldComboBox.clear()
        self.ui.columnnameFieldComboBox.clear()

        self.ui.filenameFieldComboBox.addItems(fields)
        self.ui.fileformatFieldComboBox.addItems(fields)
        self.ui.sumstatFieldComboBox.addItems(fields)
        self.ui.columnnameFieldComboBox.addItems(fields)

        candidates = ["filename", "FileName", "Filename", "FILENAME"]
        for item in candidates:
            if item in fields:
                self.ui.filenameFieldComboBox.setCurrentIndex(fields.index(item))
                break

        candidates = ["fileformat", "FileFormat", "Fileformat", "FILEFORMAT",
                      "format", "Format", "FORMAT"]
        for item in candidates:
            if item in fields:
                self.ui.fileformatFieldComboBox.setCurrentIndex(fields.index(item))
                break

        candidates = ["sumstat", "SumStat", "Sumstat", "SUMSTAT",
                      "summarystatistic", "SummaryStatistic", "Summarystatistic", "SUMMARYSTATISTIC"]
        for item in candidates:
            if item in fields:
                self.ui.sumstatFieldComboBox.setCurrentIndex(fields.index(item))
                break

        candidates = ["columnname", "ColumnName", "Columnname", "COLUMNNAME"]
        for item in candidates:
            if item in fields:
                self.ui.columnnameFieldComboBox.setCurrentIndex(fields.index(item))
                break

    def onFilenameFieldChanged(self) -> typing.NoReturn:
        '''Update Filename field
        '''
        self.updateSaveStatus(True)

    def onFileformatFieldChanged(self) -> typing.NoReturn:
        '''Update File Format field
        '''
        self.updateSaveStatus(True)

    def onSumstatFieldChanged(self) -> typing.NoReturn:
        '''Update Summary statistic field
        '''
        self.updateSaveStatus(True)

    def onColumnnameFieldChanged(self) -> typing.NoReturn:
        '''Update Column name field
        '''
        self.updateSaveStatus(True)

    # #############################################################
    # Images directory
    # #############################################################

    def onImagesSourceFileToolButtonClicked(self) -> typing.NoReturn:
        '''Manage browse for images directory
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select images directory", path)
        if dir:
            self.ui.imagesSourceFileLineEdit.setText(dir)
            settings.setValue("last_file_directory", dir)

    def onImagesSourceFileChanged(self) -> typing.NoReturn:
        '''Manage update of images directory
        '''
        dir = QtCore.QDir(self.ui.imagesSourceFileLineEdit.text())

        if dir.exists():
            self.updateSaveStatus(True)

    # #############################################################
    # Covref layer
    # #############################################################

    def onCovrefLayerToolButtonClicked(self) -> typing.NoReturn:
        '''handle browse for covref layer clicked
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open reference layer", dir, "*.shp")
        if file:
            self.ui.covrefLayerLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onCovrefLayerFileChanged(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        self.updateSaveStatus(True)

    ## #############################################################
    # Main action
    ## #############################################################

    def onComputeCovariatesButtonClicked(self) -> typing.NoReturn:
        '''ComputeCovariates computeCovariatesButton
        '''
        if not self.ui.covinputsSourceFileLineEdit.text():
            Logger.logWarning("[CovariatesProcesser] A valid covinputs source file must be provided")
            return
        else:
            if self.ui.columnnameFieldComboBox.isEnabled() and not self.ui.columnnameFieldComboBox.currentText():
                Logger.logWarning("[CovariatesProcesser] A valid columname field must be provided")
                return

            if self.ui.sumstatFieldComboBox.isEnabled() and not self.ui.sumstatFieldComboBox.currentText():
                Logger.logWarning("[CovariatesProcesser] A valid sumstat field must be provided")
                return

            if self.ui.filenameFieldComboBox.isEnabled() and not self.ui.filenameFieldComboBox.currentText():
                Logger.logWarning("[CovariatesProcesser] A valid filename field must be provided")
                return

            if self.ui.fileformatFieldComboBox.isEnabled() and not self.ui.fileformatFieldComboBox.currentText():
                Logger.logWarning("[CovariatesProcesser] A valid file format field must be provided")
                return

        if not self.ui.imagesSourceFileLineEdit.text():
            Logger.logWarning("[CovariatesProcesser] A valid image directory must be provided")
            return
        # TODO: check if images exists in the directory.

        if not self.ui.covrefLayerLineEdit.text():
            Logger.logWarning("[CovariatesProcesser] A reference source file must be provided")
            return

        try:
            covariatesProcesser = CovariatesProcesser.CovariatesProcesser()

            covariatesProcesser.input_csv = self.ui.covinputsSourceFileLineEdit.text()
            covariatesProcesser.input_csv_field_columnname = self.ui.columnnameFieldComboBox.currentText()
            covariatesProcesser.input_csv_field_sumstat = self.ui.sumstatFieldComboBox.currentText()
            covariatesProcesser.input_csv_field_filename = self.ui.filenameFieldComboBox.currentText()
            covariatesProcesser.input_csv_field_fileformat = self.ui.fileformatFieldComboBox.currentText()

            covariatesProcesser.images_directory = self.ui.imagesSourceFileLineEdit.text()

            bufferAnonLayerName = Utils.LayersName.layerName(Utils.LayersType.BUFFERSANON)
            Utils.removeLayerIfExistsByName(bufferAnonLayerName)
            bufferAnonLayer = QgsVectorLayer(self.ui.covrefLayerLineEdit.text(), bufferAnonLayerName)
            QgsProject.instance().addMapLayer(bufferAnonLayer)

            covariatesProcesser.setReferenceLayer(
                bufferAnonLayer,
                self.ui.covrefLayerLineEdit.text())

            covariatesProcesser.computeCovariates()
            Logger.logSuccess("[CovariatesProcesser] Covariates succcessfully processed at {}".format(datetime.now()))
        except:
            Logger.logWarning("[CovariatesProcesser] A problem occured while processing covariates")
