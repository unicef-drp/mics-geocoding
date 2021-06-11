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
from .mics_geocode_config_writer import mics_geocode_config_writer
from .mics_geocode_config_reader import mics_geocode_config_reader
from .mics_geocode_plugin_main_window_tab1handlery import MicsGeocodePluginMainWindowTab1Handler

from .micsgeocode import Step02Manager as step02
from .micsgeocode import CentroidsDisplacer as Displacer
from .micsgeocode.Logger import Logger

from .micsgeocode import Utils

from qgis.core import QgsVectorLayer, QgsProject  # QGIS3


class MicsGeocodePluginMainWindow(QtWidgets.QWidget):
    '''The actual window that is displayed in the qgis interface
    '''

    def __init__(self, parent, version):
        """Interface initialisation : display interface and define events"""
        self.parent = parent
        self.iface = parent.iface

        ## ####################################################################
        # Mainwindw staticinit - could not be done in qtdesigner
        ## ####################################################################

        # With or withoutl stays on top. Matter of taste.
        # QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        QtWidgets.QWidget.__init__(self, None)

        # Setup ui based on the qtdesigner form
        self.ui = Ui_MicsGeocodePluginDialog()
        self.ui.setupUi(self)

        # Initiate ui properties
        self.setFixedSize(self.width(), self.height())
        self.title = self.windowTitle() + " (" + version + ")"
        self.setWindowTitle(self.title)

        # Update position with last one used (handle switch from multiscreen to singlescrenn, change resolution, etc.)
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        pos = settings.value("WindowPosition", QtCore.QPoint(200, 200))
        wholeDisplayGeometry = QtCore.QRect(0, 0, 0, 0)
        for i in range(0, QtWidgets.QApplication.desktop().screenCount()):
            wholeDisplayGeometry = wholeDisplayGeometry.united(QtWidgets.QApplication.desktop().screen(i).geometry())
        if pos.x() > wholeDisplayGeometry.width()-50:
            pos.setX(200)
        if pos.y() > wholeDisplayGeometry.height()-50:
            pos.setY(200)

        self.move(pos)

        # Down-right logo. Here file szes and label sizes are the same, no need for scaling
        # Label size: 177 x 35
        # Could be more flexible, with an horizontal spacer or halignment settings.
        # But this level of complexity was not needed at that the time.
        pixmap = QtGui.QPixmap(":/plugins/MicsGeocodePlugin/logo_wo-unicef.png")
        self.ui.labelLogo.setPixmap(pixmap)

        # Add a validator to basename
        # see: https://doc.qt.io/qt-5/qregexpvalidator.html
        # alternative: https://doc.qt.io/qt-5/qregularexpressionvalidator.html
        regex = QtCore.QRegExp("[a-zA-Z]{0,1}[a-zA-Z0-9]{0,25}")
        validator = QtGui.QRegExpValidator(regex)
        self.ui.basenameLineEdit.setValidator(validator)

        ## ####################################################################
        # Init various members - might be overriden with config
        ## ####################################################################

        # Hold the save button status
        self.needsSave = False

        # Initiate Managers
        self.step02manager = step02.Step02Manager()
        self.displacer = Displacer.CentroidsDisplacer()

        # Hold the basename values. Made to avoid too many 'editingFinished' signal issue
        self.basename = ""
        self.ui.basenameLineEdit.clear()

        # Init output directory with tmpPath
        self.ui.outputDirLineEdit.setText(QtCore.QDir.tempPath())

        # Force tab to init at first tab. Frequent mistake when manipulating qtdesigner
        self.ui.tabWidget.setCurrentIndex(0)

        self.loadCentroidsHandler = MicsGeocodePluginMainWindowTab1Handler(self.ui)

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.basenameLineEdit.editingFinished.connect(self.onBasenameLineEditChanged)
        self.ui.outputDirToolButton.clicked.connect(self.onOutputDirToolButtonClicked)
        self.ui.outputDirLineEdit.textChanged.connect(self.onOutputDirLineEditChanged)

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

        self.ui.loadConfigButton.clicked.connect(self.onLoadConfigButtonClicked)
        self.ui.saveConfigAsButton.clicked.connect(self.onSaveConfigAsButtonClicked)
        self.ui.saveConfigButton.clicked.connect(self.onSaveConfigButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.basenameLineEdit.setToolTip("Basename for layers and file generation. Only alphanumerical characteres, and starts with a-zA-Z")
        self.ui.outputDirLineEdit.setToolTip("Output directory for shapefiles generation")
        self.ui.outputDirToolButton.setToolTip("Browse for output directory on the disk")

        self.ui.referenceLayerLineEdit.setToolTip("Browse for the reference Layer on the disk")
        self.ui.referenceLayerToolButton.setToolTip("Reference Layer on the disk")
        self.ui.ruralValuesLineEdit.setToolTip("Field description for rural values. It can receive multiple values, splitted by ';' or ',' or ' '")
        self.ui.urbanValuesLineEdit.setToolTip("Field description for urban values. It can receive multiple values, splitted by ';' or ',' or ' '")

        self.ui.centroidsLayerToolButton.setToolTip("Browse for the centroids layer on the disk")
        self.ui.centroidsLayerLineEdit.setToolTip("Browse for the centroids layer on the disk")
        self.ui.centroidsLayerNumeroFieldComboBox.setToolTip("Choose the field corresponding to cluster numero")
        self.ui.centroidsLayerTypeFieldComboBox.setToolTip("Choose the field corresponding to cluster type")

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

        ## ####################################################################
        # actually show the app
        ## ####################################################################

        # Show
        self.show()

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

    ## #############################################################
    # Close event
    ## #############################################################

    def closeEvent(self, event) -> typing.NoReturn:
        '''Save stuffs before closing
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')

        # Save current window position
        settings.setValue("WindowPosition", self.pos())

        # Ask for save
        if self.needsSave:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("The project has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.ui.saveConfigButton.click()
                event.accept()
                self.close()

            elif ret == QtWidgets.QMessageBox.Discard:
                event.accept()
                self.close()
            else:
                event.ignore()
        else:
            event.accept()
            self.close()

    ## #############################################################
    # Save Load config
    ## #############################################################

    def onLoadConfigButtonClicked(self) -> typing.NoReturn:
        '''Pick and trigger the open configuration
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open config file", dir, "*.mgc")
        if file:
            self.open(file)
            settings.setValue("last_file_directory", os.path.dirname(file))

    def open(self, fileMGC: str) -> typing.NoReturn:
        '''Open the configuration passed as an argument
        '''
        self.fileMGC = fileMGC
        self.ui.configFileLineEdit.setText(self.fileMGC)
        reader = mics_geocode_config_reader(self.fileMGC, self)
        reader.readConfig()
        self.onBasenameLineEditChanged()
        self.onOutputDirLineEditChanged()

        self.updateSaveStatus(False)

    def onSaveConfigButtonClicked(self) -> typing.NoReturn:
        '''Save the project to the current fileMGC.
           If there is none, trigger the saveas
        '''
        if not self.fileMGC:
            self.onSaveConfigAsButtonClicked()
        else:
            writer = mics_geocode_config_writer(self.fileMGC, self)
            writer.writeConfig()
            self.updateSaveStatus(False)

    def onSaveConfigAsButtonClicked(self):
        '''Pick a file and save the project to it
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save project configuration file", path, "*.mgc")
        if file:
            self.fileMGC = file
            self.ui.configFileLineEdit.setText(self.fileMGC)
            writer = mics_geocode_config_writer(self.fileMGC, self)
            writer.writeConfig()
            settings.setValue("last_file_directory", os.path.dirname(file))
            settings.setValue("last_config_file", file)
            self.updateSaveStatus(False)

    # #############################################################
    # Output directory
    # #############################################################

    def onOutputDirToolButtonClicked(self) -> typing.NoReturn:
        '''Manage browse for directory
        '''
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select output directory", path)
        if dir:
            self.outputDirectory = dir
            self.ui.outputDirLineEdit.setText(dir)
            settings.setValue("last_file_directory", dir)

    def onOutputDirLineEditChanged(self) -> typing.NoReturn:
        '''Manage update of output directory
        '''
        dir = QtCore.QDir(self.ui.outputDirLineEdit.text())

        self.ui.groupBoxCentroid.setEnabled(dir.exists())
        self.ui.groupBoxDisplacer.setEnabled(dir.exists())

        if dir.exists():
            Utils.LayersName.outputDirectory = self.ui.outputDirLineEdit.text()
            self.step02manager.setOutputDirectory(self.ui.outputDirLineEdit.text())
            self.updateSaveStatus(True)

    # #############################################################
    # Basename
    # #############################################################

    def onBasenameLineEditChanged(self) -> typing.NoReturn:
        '''Manage update basename
        '''
        # Has the basename changed ?
        # The trigger is "editingFinished, which can be triggered when the widget loses focus. Even if nothing has changed"
        if self.basename != self.ui.basenameLineEdit.text():
            self.basename = self.ui.basenameLineEdit.text()

            # The validator should prevent the text to be invalid. But hey, let's check it anyway
            if self.ui.basenameLineEdit.hasAcceptableInput():
                Utils.LayersName.basename = self.ui.basenameLineEdit.text()
                self.step02manager.setBasename(self.ui.basenameLineEdit.text())
                self.updateSaveStatus(True)
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Invalid basename")
                msgBox.setInformativeText("The basename " + self.ui.basenameLineEdit.text() + " is not valid.")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                _ = msgBox.exec_()

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
        self.step02manager.input_csv = self.ui.covinputsSourceFileLineEdit.text()
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
        self.step02manager.input_csv_field_filename = self.ui.filenameFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onFileformatFieldChanged(self) -> typing.NoReturn:
        '''Update File Format field
        '''
        self.step02manager.input_csv_field_fileformat = self.ui.fileformatFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onSumstatFieldChanged(self) -> typing.NoReturn:
        '''Update Summary statistic field
        '''
        self.step02manager.input_csv_field_sumstat = self.ui.sumstatFieldComboBox.currentText()
        self.updateSaveStatus(True)

    def onColumnnameFieldChanged(self) -> typing.NoReturn:
        '''Update Column name field
        '''
        self.step02manager.input_csv_field_columnname = self.ui.columnnameFieldComboBox.currentText()
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
            self.step02manager.images_directory = self.ui.imagesSourceFileLineEdit.text()
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
        self.step02manager.setReferenceLayer(
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

        self.step02manager.setReferenceLayer(
            layer,
            field,
            file)

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

    def onComputeCovariatesButtonClicked(self) -> typing.NoReturn:
        '''ComputeCovariates computeCovariatesButton
        '''
        self.step02manager.computeCovariates()
