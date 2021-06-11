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
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3
from .micsgeocode import CovariatesProcesser as CovariatesProcesser


class MGPMainWindowTab3Handler():
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

        self.covariatesProcesser = CovariatesProcesser.CovariatesProcesser()

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
        self.ui.covrefLayerFieldCombobox.currentTextChanged.connect(self.onCovrefLayerFieldComboboxTextChanged)

        self.ui.loadCovrefFromStep01.clicked.connect(self.onLoadCovrefFromStep01Clicked)

        self.ui.computeCovariatesButton.clicked.connect(self.onComputeCovariatesButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.covinputsSourceFileToolButton.setToolTip("Browse for the covariates inputs file on the disk")
        self.ui.covinputsSourceFileLineEdit.setToolTip("Covariates inputs file on the disk")

        self.ui.imagesSourceFileToolButton.setToolTip("Browse for the images directory on the disk")
        self.ui.imagesSourceFileLineEdit.setToolTip("Images directory on the disk")

        self.ui.filenameFieldComboBox.setToolTip("Choose the field corresponding to filename")
        self.ui.fileformatFieldComboBox.setToolTip("Choose the field corresponding to fileformat")
        self.ui.sumstatFieldComboBox.setToolTip("Choose the field corresponding to sumstat")
        self.ui.columnnameFieldComboBox.setToolTip("Choose the field corresponding to columnname")

        self.ui.covrefLayerToolButton.setToolTip("Browse for reference layer on the disk")
        self.ui.covrefLayerLineEdit.setToolTip("Reference layer on the disk")
        self.ui.covrefLayerFieldCombobox.setToolTip("Choose the field corresponding to cluster type")

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

    # #############################################################
    # Covinputs Source
    # #############################################################

    def onCovinputsSourceFileToolButtonClicked(self) -> typing.NoReturn:
        '''Browse for covinputs file
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open covinputs file", dir, "*.txt")
        if file:
            self.ui.covinputsSourceFileLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onCovinputsSourceFileChanged(self) -> typing.NoReturn:
        '''Handle new covinput file
        '''
        self.covariatesProcesser.input_csv = self.ui.covinputsSourceFileLineEdit.text()
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
        self.covariatesProcesser.input_csv_field_filename = self.ui.filenameFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onFileformatFieldChanged(self) -> typing.NoReturn:
        '''Update File Format field
        '''
        self.covariatesProcesser.input_csv_field_fileformat = self.ui.fileformatFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onSumstatFieldChanged(self) -> typing.NoReturn:
        '''Update Summary statistic field
        '''
        self.covariatesProcesser.input_csv_field_sumstat = self.ui.sumstatFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onColumnnameFieldChanged(self) -> typing.NoReturn:
        '''Update Column name field
        '''
        self.covariatesProcesser.input_csv_field_columnname = self.ui.columnnameFieldComboBox.currentText()
        self.updateSaveStatus(True)

    # #############################################################
    # Images directory
    # #############################################################

    def onImagesSourceFileToolButtonClicked(self) -> typing.NoReturn:
        '''Manage browse for images directory
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
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
            self.covariatesProcesser.images_directory = self.ui.imagesSourceFileLineEdit.text()
            self.updateSaveStatus(True)

    # #############################################################
    # Covref layer
    # #############################################################

    def onCovrefLayerToolButtonClicked(self) -> typing.NoReturn:
        '''handle browse for covref layer clicked
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open reference layer", dir, "*.shp")
        if file:
            self.ui.covrefLayerLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onCovrefLayerFileChanged(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        fields = Utils.getFieldsListAsStrArray(self.ui.covrefLayerLineEdit.text())
        if fields:
            self.ui.covrefLayerFieldCombobox.addItems(fields)
            self.ui.covrefLayerFieldCombobox.setEnabled(True)
            self.ui.covrefLayerFieldCombobox.setCurrentIndex(0)

            candidates = ["cluster", "Cluster", "CLUSTER"]
            for item in candidates:
                if item in fields:
                    self.ui.covrefLayerFieldCombobox.setCurrentIndex(fields.index(item))
                    break
        else:
            self.ui.covrefLayerFieldCombobox.setEnabled(False)

        self.updateSaveStatus(True)

    def onCovrefLayerFieldComboboxTextChanged(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        self.covariatesProcesser.setReferenceLayer(
            None,
            self.ui.covrefLayerFieldCombobox.currentText(),
            self.ui.covrefLayerLineEdit.text())

        self.updateSaveStatus(True)

    def onLoadCovrefFromStep01Clicked(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        field = 'cluster'
        file = Utils.LayersName.fileName(Utils.LayersType.BUFFERSANON)
        Logger.logInfo("@" + file + "@")
        layer = None
        layers = QgsProject.instance().mapLayersByName(Utils.LayersName.layerName(Utils.LayersType.BUFFERSANON))
        if layers:
            layer = layers[0]
        self.ui.covrefLayerLineEdit.setText(file)
        index = self.ui.covrefLayerFieldCombobox.findText(field)
        if index > -1:
            self.ui.covrefLayerFieldCombobox.setCurrentIndex(index)

        self.covariatesProcesser.setReferenceLayer(
            layer,
            field,
            file)

    def onComputeCovariatesButtonClicked(self) -> typing.NoReturn:
        '''ComputeCovariates computeCovariatesButton
        '''
        self.covariatesProcesser.computeCovariates()
