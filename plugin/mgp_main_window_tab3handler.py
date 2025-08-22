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
from PyQt5 import QtWidgets, QtCore
import typing

from .mgp_file import openFile as MGP_OPEN_FILE
from .micsgeocode.Logger import Logger
from .micsgeocode import Utils
from qgis.core import QgsVectorLayer, QgsProject  # QGIS3
from .micsgeocode import CovariatesProcesser as CovariatesProcesser


class MGPMainWindowTab3Handler(QtCore.QObject):
    '''The actual window that is displayed in the qgis interface
    '''

    def __init__(self, mainwindow):
        """Interface initialisation : display interface and define events"""
        super().__init__()
        self.mainwindow = mainwindow
        self.ui = self.mainwindow.ui
        self.covoutputs_file = None
        self.ui.covoutputsOpenFileToolButton.setEnabled(False)
        self.ui.covinputsOpenSourceFileToolButton.setEnabled(False)

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.covinputsSourceFileToolButton.clicked.connect(self.onCovinputsSourceFileToolButtonClicked)
        self.ui.covinputsSourceFileLineEdit.textChanged.connect(self.onCovinputsSourceFileChanged)
        self.ui.covinputsOpenSourceFileToolButton.clicked.connect(self.onCovinputsOpenSourceFileToolButtonClicked)

        self.ui.imagesSourceFileToolButton.clicked.connect(self.onImagesSourceFileToolButtonClicked)
        self.ui.imagesSourceFileLineEdit.textChanged.connect(self.onImagesSourceFileChanged)

        self.ui.filenameFieldComboBox.currentTextChanged.connect(self.onFilenameFieldChanged)
        self.ui.fileformatFieldComboBox.currentTextChanged.connect(self.onFileformatFieldChanged)
        self.ui.sumstatFieldComboBox.currentTextChanged.connect(self.onSumstatFieldChanged)
        self.ui.columnnameFieldComboBox.currentTextChanged.connect(self.onColumnnameFieldChanged)
        self.ui.nodataFieldComboBox.currentTextChanged.connect(self.onNodataFieldChanged)

        self.ui.covrefLayerToolButton.clicked.connect(self.onCovrefLayerToolButtonClicked)
        self.ui.covrefLayerLineEdit.textChanged.connect(self.onCovrefLayerFileChanged)
        self.ui.covrefLayerIdFieldCombobox.currentTextChanged.connect(self.onCovrefLayerIdFieldComboboxTextChanged)

        self.ui.computeCovariatesButton.clicked.connect(self.onComputeCovariatesButtonClicked)
        self.ui.covoutputsOpenFileToolButton.clicked.connect(self.onCovoutputsOpenFileToolButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.covinputsSourceFileToolButton.setToolTip("Browse for covariates input file on the computer. Must be CSV file.")
        self.ui.covinputsSourceFileLineEdit.setToolTip("Covariates input file on the computer.")
        self.ui.covinputsOpenSourceFileToolButton.setToolTip("Open covariates input file.")

        self.ui.imagesSourceFileToolButton.setToolTip("Browse for covariates input folder on the computer. Must contain image files listed in the “Covariates Input File”.")
        self.ui.imagesSourceFileLineEdit.setToolTip("Covariates input folder on the computer.")

        self.ui.filenameFieldComboBox.setToolTip("Choose the field indicating file name variable.")
        self.ui.fileformatFieldComboBox.setToolTip("Choose the field indicating file format variable.")
        self.ui.sumstatFieldComboBox.setToolTip("Choose the field indicating summary statistics variable.")
        self.ui.columnnameFieldComboBox.setToolTip("Choose the field indicating variable name variable.")
        self.ui.nodataFieldComboBox.setToolTip("Choose the field indicating raster no-data value variable.")

        self.ui.covrefLayerToolButton.setToolTip("Browse for the anonymised cluster buffer shapefile on the computer. It was generated to phase of cluster displacement (Displace).")
        self.ui.covrefLayerLineEdit.setToolTip("Anonymised cluster buffer shapefile on the computer.")
        self.ui.covrefLayerIdFieldCombobox.setToolTip("Choose the field corresponding to the polygon layer's ID field.")

        self.ui.computeCovariatesButton.setToolTip("Compute covariates. QGIS generates additional layers depending on inputs and a CSV file with the outputs.")

        ## ####################################################################
        # Init icons
        ## ####################################################################

        self.ui.covinputsOpenSourceFileToolButton.setIcon(
            self.ui.covinputsOpenSourceFileToolButton.style().standardIcon(getattr(QtWidgets.QStyle, "SP_DirOpenIcon"))
        )
        self.ui.covoutputsOpenFileToolButton.setIcon(
            self.ui.covoutputsOpenFileToolButton.style().standardIcon(getattr(QtWidgets.QStyle, "SP_DirOpenIcon"))
        )

        self.NOT_AVAILABLE_VALUE = 'Not available'

    ## #############################################################
    # reset
    ## #############################################################

    def reset(self) -> typing.NoReturn:
        self.ui.covinputsSourceFileLineEdit.clear()
        self.ui.imagesSourceFileLineEdit.clear()
        self.ui.covrefLayerLineEdit.clear()
        self.ui.covoutputsOpenFileToolButton.setEnabled(False)
        self.covoutputs_file = None

    ## #############################################################
    # Load covref from step2
    ## #############################################################

    def loadCovrefFromStep02(self) -> typing.NoReturn:
        '''handle reference layer changed
        '''
        file = Utils.LayersName.fileName(Utils.LayersType.BUFFERSANON)
        layers = QgsProject.instance().mapLayersByName(Utils.LayersName.layerName(Utils.LayersType.BUFFERSANON))
        if layers:
            self.ui.covrefLayerLineEdit.setText(file)
        else:
            self.ui.covrefLayerLineEdit.clear()

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
        self.mainwindow.updateSaveStatus(True)
        if self.ui.covinputsSourceFileLineEdit.text():
            self.ui.covinputsOpenSourceFileToolButton.setEnabled(True)
        else:
            self.ui.covinputsOpenSourceFileToolButton.setEnabled(False)

    def onCovinputsOpenSourceFileToolButtonClicked(self) -> typing.NoReturn:
        '''Open covinput file on disk
        '''
        if self.ui.covinputsSourceFileLineEdit.text():
            MGP_OPEN_FILE(self.ui.covinputsSourceFileLineEdit.text())

    def updateCovinputsComboBoxes(self):

        # Define candidates for each field
        # These are normalized candidates, without spaces or underscores, to match the fields in the CSV
        candidates = {
            "filename": ["filename", "name", 'file'],
            "fileformat": ["fileformat", "format"],
            "sumstat": ["sumstat", "sumstats", "summarystatistic", "summarystatistics", "sumstatistics"],
            "columnname": ["columnname", "variablename", "varname"],
            "nodata": ['rasternodatavalue', 'rasternodata', 'nodatavalue', 'nodata']
        }

        # Retrieve fieldlist and populate comboboxes
        fields = Utils.getFieldsListAsStrArray(self.ui.covinputsSourceFileLineEdit.text())
        fields_and_notavailable = fields + [self.NOT_AVAILABLE_VALUE]  # Add 'Not available' to allow for no selection (optional field)

        Utils.setComboBox(self.ui.filenameFieldComboBox, candidates['filename'], fields)
        Utils.setComboBox(self.ui.fileformatFieldComboBox, candidates['fileformat'], fields)
        Utils.setComboBox(self.ui.sumstatFieldComboBox, candidates['sumstat'], fields)
        Utils.setComboBox(self.ui.columnnameFieldComboBox, candidates['columnname'], fields)
        Utils.setComboBox(self.ui.nodataFieldComboBox, candidates['nodata'], fields_and_notavailable, self.NOT_AVAILABLE_VALUE)

    def onFilenameFieldChanged(self) -> typing.NoReturn:
        '''Update Filename field
        '''
        self.mainwindow.updateSaveStatus(True)

    def onFileformatFieldChanged(self) -> typing.NoReturn:
        '''Update File Format field
        '''
        self.mainwindow.updateSaveStatus(True)

    def onSumstatFieldChanged(self) -> typing.NoReturn:
        '''Update Summary statistic field
        '''
        self.mainwindow.updateSaveStatus(True)

    def onColumnnameFieldChanged(self) -> typing.NoReturn:
        '''Update Column name field
        '''
        self.mainwindow.updateSaveStatus(True)

    def onNodataFieldChanged(self) -> typing.NoReturn:
        '''Update No data name field
        '''
        self.mainwindow.updateSaveStatus(True)

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
        self.mainwindow.updateSaveStatus(True)

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
        self.ui.covrefLayerIdFieldCombobox.clear()
        self.updateCovrefLayerIdFieldCombobox()
        self.mainwindow.updateSaveStatus(True)

    def updateCovrefLayerIdFieldCombobox(self):
        # retrieve field and update combobox
        fields = Utils.getFieldsListAsStrArray(self.ui.covrefLayerLineEdit.text())
        if fields:
            self.ui.covrefLayerIdFieldCombobox.addItems(fields)
            self.ui.covrefLayerIdFieldCombobox.setEnabled(True)
            self.ui.covrefLayerIdFieldCombobox.setCurrentIndex(0)
            #TODO: set 'cluster' field name by default if exists
        else:
            self.ui.covrefLayerIdFieldCombobox.setEnabled(False)
    
    def onCovrefLayerIdFieldComboboxTextChanged(self) -> typing.NoReturn:
        '''handle reference field changed
        '''
        self.mainwindow.updateSaveStatus(True)

    ## #############################################################
    # Main action
    ## #############################################################

    def onCovoutputsOpenFileToolButtonClicked(self) -> typing.NoReturn:
        if self.covoutputs_file:
            MGP_OPEN_FILE(self.covoutputs_file)

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

            if self.ui.nodataFieldComboBox.isEnabled() and self.ui.nodataFieldComboBox.currentText() == self.NOT_AVAILABLE_VALUE:
                Logger.logInfo("[CovariatesProcesser] Raster's nodata value field is not provided, the original value from the raster will be used.")
            
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
            covariatesProcesser.input_csv_field_nodata = None if self.ui.nodataFieldComboBox.currentText() == self.NOT_AVAILABLE_VALUE else self.ui.nodataFieldComboBox.currentText()

            covariatesProcesser.images_directory = self.ui.imagesSourceFileLineEdit.text()

            # Read the name of the buffer shapefile used for the covariate calculation
            bufferShpPath = self.ui.covrefLayerLineEdit.text()
            # Extract its name without extension and set is as layer name
            bufferLayerName, extension = os.path.splitext(os.path.basename(bufferShpPath))
            #bufferLayerName = Utils.LayersName.layerName(Utils.LayersType.BUFFERSANON)
            # Remove the layer is if it already exists and load the new one
            Utils.removeLayerIfExistsByName(bufferLayerName)
            bufferLayer = QgsVectorLayer(bufferShpPath, bufferLayerName)
            QgsProject.instance().addMapLayer(bufferLayer)
            bufferIdField = self.ui.covrefLayerIdFieldCombobox.currentText()

            covariatesProcesser.setReferenceLayer(
                bufferLayer,
                bufferShpPath,
                bufferIdField)

            covariatesProcesser.computeCovariates()
            self.covoutputs_file = covariatesProcesser.output_file
            if self.covoutputs_file:
                self.ui.covoutputsOpenFileToolButton.setEnabled(True)
            else:
                self.ui.covoutputsOpenFileToolButton.setEnabled(False)

            if covariatesProcesser.output_warning != '':
                Logger.logWarning("[CovariatesProcesser] " + covariatesProcesser.output_warning)
            else:
                Logger.logSuccess("[CovariatesProcesser] Covariates succcessfully processed")

        except BaseException as e:
            Logger.logException("[CovariatesProcesser] A problem occured while processing covariates.", e)
