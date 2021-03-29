# coding: utf-8

# selectpointsdialog.py ---
#
# Author: etienne
# Created: jeu. avril 21 11:15:56 2016 (+0200)
# Version:

import os

from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
import re

from .ui_mics_geocode_plugin_dialog import Ui_MicsGeocodePluginDialog
from .mics_geocode_config_writer import mics_geocode_config_writer
from .mics_geocode_config_reader import mics_geocode_config_reader
from .micsgeocode import Step01Manager as step01
from .micsgeocode import Step02Manager as step02
from .micsgeocode.Logger import Logger
# from .micsgeocode import mics_step02_extract_covariates as step02
from .micsgeocode import Utils


class MicsGeocodePluginMainWindow(QtWidgets.QWidget):
    def __init__(self, parent, version):
        """Interface initialisation : display interface and define events"""
        self.parent = parent
        self.iface = parent.iface
        # QtWidgets.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        QtWidgets.QWidget.__init__(self, None)
        self.ui = Ui_MicsGeocodePluginDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.title = self.windowTitle() + " (" + version + ")"
        self.setWindowTitle(self.title)
        self.needsSave = False

        pixmap = QtGui.QPixmap(":/plugins/MicsGeocodePlugin/logo_nobg.png")
        self.ui.labelLogo.setPixmap(pixmap)

        self.step01manager = step01.Step01Manager()
        self.step02manager = step02.Step02Manager()

        self.fileMGC = ""

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

        regex = QtCore.QRegExp("[a-zA-Z][a-zA-Z0-9]{0,15}")
        validator = QtGui.QRegExpValidator(regex)
        self.ui.basenameLineEdit.setValidator(validator)

        # Signals Slots
        self.ui.basenameLineEdit.editingFinished.connect(self.onBasenameLineEditChanged)
        self.ui.outputDirToolButton.clicked.connect(self.onOutputDirToolButtonClicked)
        self.ui.outputDirLineEdit.textChanged.connect(self.onOutputDirLineEditChanged)

        self.ui.referenceLayerToolButton.clicked.connect(self.onReferenceLayerToolButtonClicked)
        self.ui.referenceLayerLineEdit.textChanged.connect(self.onReferenceLayerFileChanged)
        self.ui.referenceLayerFieldCombobox.currentTextChanged.connect(self.onReferenceLayerFieldComboboxTextChanged)
        self.ui.ruralValuesLineEdit.textChanged.connect(self.onRuralValuesLineEditChanged)
        self.ui.urbanValuesLineEdit.textChanged.connect(self.onUrbanValuesLineEditChanged)

        self.ui.centroidsSourceFileToolButton.clicked.connect(self.onCentroidsSourceFileToolButtonClicked)
        self.ui.centroidsSourceFileLineEdit.textChanged.connect(self.onCentroidsSourceFileChanged)
        self.ui.loadCentroidsButton.clicked.connect(self.onLoadCentroidsButtonCLicked)

        self.ui.longitudeFieldComboBox.currentTextChanged.connect(self.onLongitudeFieldChanged)
        self.ui.latitudeFieldComboBox.currentTextChanged.connect(self.onLatitudeFieldChanged)
        self.ui.numeroFieldComboBox.currentTextChanged.connect(self.onNumeroFieldChanged)
        self.ui.typeFieldComboBox.currentTextChanged.connect(self.onTypeFieldChanged)

        self.ui.longitudeFieldLineEdit.textChanged.connect(self.onLongitudeFieldLEChanged)
        self.ui.latitudeFieldLineEdit.textChanged.connect(self.onLatitudeFieldLEChanged)
        self.ui.numeroFieldLineEdit.textChanged.connect(self.onNumeroFieldLEChanged)
        self.ui.typeFieldLineEdit.textChanged.connect(self.onTypeFieldLEChanged)

        self.ui.displaceCentroidsButton.clicked.connect(self.onDisplaceCentroidsButtonClicked)

        self.ui.loadConfigButton.clicked.connect(self.onLoadConfigButtonClicked)
        self.ui.saveConfigAsButton.clicked.connect(self.onsaveConfigAsButtonClicked)
        self.ui.saveConfigButton.clicked.connect(self.onsaveConfigButtonClicked)

        # Tooltips
        self.ui.referenceLayerLineEdit.setToolTip("Browser for the reference Layer on the disk")
        self.ui.referenceLayerToolButton.setToolTip("Browser for the reference Layer on the disk")
        self.ui.ruralValuesLineEdit.setToolTip("Field description for rural values. It can receive multiple values, splitted by ';' or ',' or ' '")
        self.ui.urbanValuesLineEdit.setToolTip("Field description for urban values. It can receive multiple values, splitted by ';' or ',' or ' '")

        self.ui.centroidsSourceFileToolButton.setToolTip("Browser for the centroids layer on the disk")
        self.ui.centroidsSourceFileLineEdit.setToolTip("Browser for the centroids layer on the disk")

        self.ui.longitudeFieldComboBox.setToolTip("Choose the field corresponding to longitude")
        self.ui.longitudeFieldLineEdit.setToolTip("Choose the field corresponding to longitude")

        self.ui.latitudeFieldComboBox.setToolTip("Choose the field corresponding to latitude")
        self.ui.latitudeFieldLineEdit.setToolTip("Choose the field corresponding to latitude")

        self.ui.numeroFieldComboBox.setToolTip("Choose the field corresponding to cluster numero")
        self.ui.numeroFieldLineEdit.setToolTip("Choose the field corresponding to cluster numero")

        self.ui.typeFieldComboBox.setToolTip("Choose the field corresponding to cluster type")
        self.ui.typeFieldLineEdit.setToolTip("Choose the field corresponding to cluster type")

        # Gui Init Values - here.
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.basenameLineEdit.setText("basename")
        self.ui.outputDirLineEdit.setText(QtCore.QDir.tempPath())

        # config management
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        configFile = settings.value("last_config_file", "")
        if configFile != "" and os.path.exists(configFile):
            self.open(configFile)

        # Show
        self.show()

        self.updateSaveStatus(True)
        self.ui.saveConfigButton.click()


    ## #############################################################
    # Close events
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> None:
        self.needsSave = needsSave
        self.ui.saveConfigButton.setEnabled(self.needsSave)

    ## #############################################################
    # Close events
    ## #############################################################

    # Save Configuration
    def closeEvent(self, event):
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        settings.setValue("WindowPosition", self.pos())

        if self.needsSave:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("The project has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.ui.saveConfigButton.click()
                self.close()
            elif ret == QtWidgets.QMessageBox.Discard:
                self.close()
        else:
            self.close()

    # Open / Save events
    def onLoadConfigButtonClicked(self):
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open config file", dir, "*.mgc")
        if file:
            self.open(file)
            settings.setValue("last_file_directory", os.path.dirname(file))
            settings.setValue("last_config_file", file)

    def open(self, fileMGC):
        self.fileMGC = fileMGC
        reader = mics_geocode_config_reader(self.fileMGC, self)
        reader.readConfig()
        self.ui.loadCentroidsButton.click()
        self.ui.displaceCentroidsButton.click()
        self.updateSaveStatus(False)

    def onsaveConfigButtonClicked(self):
        writer = mics_geocode_config_writer(self.fileMGC, self)
        writer.writeConfig()
        self.updateSaveStatus(False)

    def onsaveConfigAsButtonClicked(self):
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save centroids file", path, "*.mgc")
        if file:
            self.fileMGC = file
            writer = mics_geocode_config_writer(self.fileMGC, self)
            writer.writeConfig()
            settings.setValue("last_file_directory", os.path.dirname(file))
            settings.setValue("last_config_file", file)
            self.updateSaveStatus(False)

    # #############################################################
    # Output directory
    # #############################################################

    def onOutputDirToolButtonClicked(self):
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select output directory", path)
        if dir:
            self.outputDirectory = dir
            self.ui.outputDirLineEdit.setText(dir)
            settings.setValue("last_file_directory", dir)

    def onOutputDirLineEditChanged(self):
        dir = QtCore.QDir(self.ui.outputDirLineEdit.text())

        self.ui.groupBoxCentroid.setEnabled(dir.exists())
        self.ui.groupBoxDisplacer.setEnabled(dir.exists())

        if dir.exists():
            self.step01manager.setOutputsDirectory(self.ui.outputDirLineEdit.text())
            self.updateSaveStatus(True)

    # #############################################################
    # Centroids Source
    # #############################################################

    def onBasenameLineEditChanged(self):
        if self.ui.basenameLineEdit.hasAcceptableInput():
            Logger.logInfo("PASPSPAPAPSAPSAPPSAPSAPSALLLLLLL YES")
            self.step01manager.setBasename(self.ui.basenameLineEdit.text())
            self.updateSaveStatus(True)
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Invalid basename")
            msgBox.setInformativeText("The basename " + self.ui.basenameLineEdit.text() + " is not valid.")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec_()

    # #############################################################
    # Centroids Source
    # #############################################################

    def onCentroidsSourceFileToolButtonClicked(self):
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open centroids file", dir, "*")
        if file:
            self.centroidsFile = file
            self.ui.centroidsSourceFileLineEdit.setText(os.path.normpath(self.centroidsFile))
            settings.setValue("last_file_directory",os.path.dirname(self.centroidsFile))

    def onCentroidsSourceFileChanged(self):
        Logger.logInfo("centroids file changed: " + self.ui.centroidsSourceFileLineEdit.text())
        fields = Utils.getFieldsListAsStrArray(self.ui.centroidsSourceFileLineEdit.text())

        if len(fields) > 1:
            self.ui.stackFields.setCurrentIndex(1)
        else:
            self.ui.stackFields.setCurrentIndex(0)

        self.step01manager.setCentroidFile(self.ui.centroidsSourceFileLineEdit.text())

        extension = Path(self.ui.centroidsSourceFileLineEdit.text()).suffix[1:]
        self.ui.typeFieldComboBox.clear()
        self.ui.numeroFieldComboBox.clear()
        self.ui.longitudeFieldComboBox.clear()
        self.ui.latitudeFieldComboBox.clear()

        self.ui.typeFieldComboBox.addItems(fields)
        candidates = ["Type", "type", "TYPE"]
        for item in candidates:
            if item in fields:
                self.ui.typeFieldComboBox.setCurrentIndex(fields.index(item))
                break

        self.ui.numeroFieldComboBox.addItems(fields)
        candidates = ["clusterno", "ClusterNo", "CLUSTERNO"]
        for item in candidates:
            if item in fields:
                self.ui.numeroFieldComboBox.setCurrentIndex(fields.index(item))
                break

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

        self.ui.loadCentroidsButton.click()

        self.updateSaveStatus(True)

    def onLoadCentroidsButtonCLicked(self):
        self.step01manager.loadCentroids()

    def onLongitudeFieldChanged(self) -> None:
        self.step01manager.setLongField(self.ui.longitudeFieldComboBox.currentText())
        self.updateSaveStatus(True)

    def onLatitudeFieldChanged(self) -> None:
        self.step01manager.setLatField(self.ui.latitudeFieldComboBox.currentText())
        self.updateSaveStatus(True)

    def onNumeroFieldChanged(self) -> None:
        self.step01manager.setClusterNoField(self.ui.numeroFieldComboBox.currentText())
        self.updateSaveStatus(True)

    def onTypeFieldChanged(self) -> None:
        self.step01manager.setClusterTypeField(self.ui.typeFieldComboBox.currentText())
        self.updateSaveStatus(True)

    def onLongitudeFieldLEChanged(self) -> None:
        self.step01manager.setLongField(self.ui.longitudeFieldLineEdit.text())
        self.updateSaveStatus(True)

    def onLatitudeFieldLEChanged(self) -> None:
        self.step01manager.setLatField(self.ui.latitudeFieldLineEdit.text())
        self.updateSaveStatus(True)

    def onNumeroFieldLEChanged(self) -> None:
        self.step01manager.setClusterNoField(self.ui.numeroFieldLineEdit.text())
        self.updateSaveStatus(True)

    def onTypeFieldLEChanged(self) -> None:
        self.step01manager.setClusterTypeField(self.ui.typeFieldLineEdit.text())
        self.updateSaveStatus(True)

    # #############################################################
    # Reference Layer
    # #############################################################

    def onReferenceLayerToolButtonClicked(self):
        settings = QtCore.QSettings('MicsGeocode', 'qgis plugin')
        dir = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open reference layer", dir, "*")
        if file:
            self.ui.referenceLayerLineEdit.setText(os.path.normpath(file))
            settings.setValue("last_file_directory", os.path.dirname(file))

    def onReferenceLayerFileChanged(self):

        Logger.logInfo("[CHANGING: ] " + self.ui.referenceLayerLineEdit.text())

        self.step01manager.setReferenceLayer(self.ui.referenceLayerLineEdit.text())
        self.ui.referenceLayerFieldCombobox.clear()

        fields = Utils.getFieldsListAsStrArray(self.ui.referenceLayerLineEdit.text())
        if fields:
            self.ui.referenceLayerFieldCombobox.addItems(fields)
            self.ui.referenceLayerFieldCombobox.setEnabled(True)
        else:
            self.ui.referenceLayerFieldCombobox.setEnabled(False)

        self.updateSaveStatus(True)

    def onReferenceLayerFieldComboboxTextChanged(self):
        self.step01manager.setReferenceLayerField(self.ui.referenceLayerFieldCombobox.currentText())
        self.updateSaveStatus(True)

    def onUrbanValuesLineEditChanged(self):
        list = re.split(';|,| ',self.ui.urbanValuesLineEdit.text())
        self.step01manager.setUrbanTypes([x for x in list if x])
        self.updateSaveStatus(True)

    def onRuralValuesLineEditChanged(self):
        list = re.split(';|,| ',self.ui.ruralValuesLineEdit.text())
        self.step01manager.setRuralTypes([x for x in list if x])
        self.updateSaveStatus(True)

    ## #############################################################
    # Admin boundaries
    ## #############################################################

    def onDisplaceCentroidsButtonClicked(self):
        self.step01manager.setReferenceLayer(self.ui.referenceLayerLineEdit.text())
        self.step01manager.displaceCentroids()
