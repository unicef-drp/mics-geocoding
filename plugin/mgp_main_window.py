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
from .mgp_config_writer import mgp_config_writer
from .mgp_config_reader import mgp_config_reader
from .mgp_main_window_tab1handler import MGPMainWindowTab1Handler
from .mgp_main_window_tab2handler import MGPMainWindowTab2Handler
from .mgp_main_window_tab3handler import MGPMainWindowTab3Handler

from .micsgeocode.Logger import Logger

from .micsgeocode import Utils

from qgis.core import QgsVectorLayer, QgsProject  # QGIS3


class MGPMainWindow(QtWidgets.QMainWindow):
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
        QtWidgets.QMainWindow.__init__(self, None)

        # Setup ui based on the qtdesigner form
        self.ui = Ui_MGPDialog()
        self.ui.setupUi(self)

        # Init Logger
        Logger.widget = self.ui.l_status

        # Initiate ui properties
        self.setFixedSize(self.width(), self.height())
        self.title = self.windowTitle() + " (" + version + ")"
        self.setWindowTitle(self.title)

        # Add a validator to basename
        # see: https://doc.qt.io/qt-5/qregexpvalidator.html
        # alternative: https://doc.qt.io/qt-5/qregularexpressionvalidator.html
        regex = QtCore.QRegExp("[a-zA-Z]{0,1}[a-zA-Z0-9]{0,25}")
        validator = QtGui.QRegExpValidator(regex)
        self.ui.basenameLineEdit.setValidator(validator)

        ## ####################################################################
        # Init various members - might be overriden with config
        ## ####################################################################

        self.loadCentroidsHandler = MGPMainWindowTab1Handler(self)
        self.displaceCentroidsHandler = MGPMainWindowTab2Handler(self)
        self.covariatesHandler = MGPMainWindowTab3Handler(self)

        ## ####################################################################
        # handle menubar
        ## ####################################################################

        self.ui.actionnew.setIcon(
            self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_FileDialogNewFolder"))
        )

        self.ui.actionopen.setIcon(
            self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_DialogOpenButton"))
        )

        self.ui.actionsave.setIcon(
            self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_DialogSaveButton"))
        )

        self.ui.actionrun.setIcon(
            self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay"))
        )

        self.ui.actionnew.triggered.connect(self.onNewConfigTriggered)
        self.ui.actionopen.triggered.connect(self.onOpenConfigTriggered)
        self.ui.actionopenmostrecent.triggered.connect(self.onOpenMostRecentConfigTriggered)
        self.ui.actionsave.triggered.connect(self.onSaveConfigTriggered)
        self.ui.actionsaveas.triggered.connect(self.onSaveConfigAsTriggered)

        self.ui.actionrun.triggered.connect(self.onRunTriggered)

        self.ui.actionGenerate.triggered.connect(self.onFocusOnGenerateTriggered)
        self.ui.actionDisplace.triggered.connect(self.onFocusOnDisplaceTriggered)
        self.ui.actionExtract.triggered.connect(self.onFocusOnExtractTriggered)

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.basenameLineEdit.editingFinished.connect(self.onBasenameLineEditChanged)
        self.ui.outputDirToolButton.clicked.connect(self.onOutputDirToolButtonClicked)
        self.ui.outputDirLineEdit.textChanged.connect(self.onOutputDirLineEditChanged)

        self.loadCentroidsHandler.centroidsLoaded.connect(self.displaceCentroidsHandler.loadCentroidsFromStep01)
        self.displaceCentroidsHandler.centroidsDisplaced.connect(self.covariatesHandler.loadCovrefFromStep02)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.basenameLineEdit.setToolTip("Basename of layers and file generation. Only alphanumerical characters")

        self.ui.outputDirLineEdit.setToolTip("Output directory for shapefiles generation")
        self.ui.outputDirToolButton.setToolTip("Browse for output directory on the disk")

        ## ####################################################################
        # init all var
        ## ####################################################################

        self.reset()

        ## ####################################################################
        # actually show the app
        ## ####################################################################

        # Show
        self.show()

        self.updateSaveStatus(False)

    ## #############################################################
    # update save status
    ## #############################################################

    def updateSaveStatus(self, needsSave: bool) -> typing.NoReturn:
        self.needsSave = needsSave
        if self.needsSave:
            self.setWindowTitle(self.title + " * ")
        else:
            self.setWindowTitle(self.title)

    # #############################################################
    # Reset
    # #############################################################

    def reset(self) -> typing.NoReturn:
        # Hold the save button status
        self.fileMGC = None

        # Hold the basename values. Made to avoid too many 'editingFinished' signal issue
        self.basename = ""
        self.ui.basenameLineEdit.clear()

        # Init output directory with tmpPath
        self.ui.outputDirLineEdit.setText(QtCore.QDir.toNativeSeparators(QtCore.QDir.tempPath()))
        # Auto update output directory with default values
        self.onOutputDirLineEditChanged()

        # Force tab to init at first tab. Frequent mistake when manipulating qtdesigner
        self.ui.tabWidget.setCurrentIndex(0)

        # tabs
        self.loadCentroidsHandler.reset()
        self.displaceCentroidsHandler.reset()
        self.covariatesHandler.reset()

        # update save status
        self.updateSaveStatus(False)

    ## #############################################################
    # Close event
    ## #############################################################

    def saveIfNeeded(self) -> bool:
        '''Save stuff before opening new project
           Return a keepgoing or not.
        '''
        # Ask for save
        if self.needsSave:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("The current project has been modified")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Save:
                self.ui.actionsave.trigger()
                return True

            elif ret == QtWidgets.QMessageBox.Discard:
                return True
            else:
                return False
        else:
            return True

    def closeEvent(self, event) -> typing.NoReturn:
        '''Save stuffs before closing
        '''
        # Ask for save, that returns a boolean that concern the event processing
        if self.saveIfNeeded():
            event.accept()
            self.close()
        else:
            event.ignore()

    ## #############################################################
    # Run current tab
    ## #############################################################

    def onRunTriggered(self):
        if self.ui.tabWidget.currentIndex() == 0:
            self.ui.loadCentroidsButton.click()
        elif self.ui.tabWidget.currentIndex() == 1:
            self.ui.displaceCentroidsButton.click()
        elif self.ui.tabWidget.currentIndex() == 2:
            self.ui.computeCovariatesButton.click()

    ## #############################################################
    # Switch tab
    ## #############################################################

    def onFocusOnGenerateTriggered(self) -> typing.NoReturn:
        '''Focus on the 1st tab, generate
        '''
        self.ui.tabWidget.setCurrentIndex(0)

    def onFocusOnDisplaceTriggered(self) -> typing.NoReturn:
        '''Focus on the 2nd tab, displace
        '''
        self.ui.tabWidget.setCurrentIndex(1)

    def onFocusOnExtractTriggered(self) -> typing.NoReturn:
        '''Focus on the 3rd tab, extract
        '''
        self.ui.tabWidget.setCurrentIndex(2)

   ## #############################################################
   # Save Load config
   ## #############################################################

    def onNewConfigTriggered(self) -> typing.NoReturn:
        '''Trigger the new configuration
        '''
        if self.saveIfNeeded():
            self.reset()
            self.onSaveConfigAsTriggered()

    def onOpenConfigTriggered(self) -> typing.NoReturn:
        '''Pick and trigger the open configuration
        '''
        if self.saveIfNeeded():
            settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
            dir = settings.value("last_file_directory", QtCore.QDir.homePath())
            file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open config file", dir, "*.mgc")
            if file:
                self.open(file)
                settings.setValue("last_file_directory", os.path.dirname(file))
                Logger.logSuccess("Project " + QtCore.QFileInfo(self.fileMGC).fileName() + " opened")

    def onOpenMostRecentConfigTriggered(self) -> typing.NoReturn:
        '''Pick and trigger the open configuration
        '''
        if self.saveIfNeeded():
            settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
            lastOpened = settings.value("last_config_file")
            if lastOpened:
                self.open(lastOpened)
                settings.setValue("last_file_directory", os.path.dirname(lastOpened))
                Logger.logSuccess("Project " + QtCore.QFileInfo(self.fileMGC).fileName() + " opened")

    def open(self, fileMGC: str) -> typing.NoReturn:
        '''Open the configuration passed as an argument
        '''
        self.fileMGC = fileMGC
        self.ui.configFileLineEdit.setText(self.fileMGC)
        reader = mgp_config_reader(self.fileMGC, self)
        reader.readConfig()
        self.onBasenameLineEditChanged()
        self.onOutputDirLineEditChanged()

        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        settings.setValue("last_config_file", self.fileMGC)

        self.updateSaveStatus(False)

    def onSaveConfigTriggered(self) -> typing.NoReturn:
        '''Save the project to the current fileMGC.
           If there is none, trigger the saveas
        '''
        if not self.fileMGC:
            self.onSaveConfigAsTriggered()
        else:
            writer = mgp_config_writer(self.fileMGC, self)
            writer.writeConfig()
            self.updateSaveStatus(False)
            Logger.logSuccess("Project " + QtCore.QFileInfo(self.fileMGC).fileName() + " saved")

    def onSaveConfigAsTriggered(self):
        '''Pick a file and save the project to it
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        file, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save project configuration file", path, "*.mgc")
        if file:
            self.fileMGC = file
            self.ui.configFileLineEdit.setText(self.fileMGC)
            writer = mgp_config_writer(self.fileMGC, self)
            writer.writeConfig()
            settings.setValue("last_file_directory", os.path.dirname(file))
            settings.setValue("last_config_file", file)
            self.updateSaveStatus(False)
            Logger.logSuccess("Project " + QtCore.QFileInfo(self.fileMGC).fileName() + " saved")

    # #############################################################
    # Output directory
    # #############################################################

    def onOutputDirToolButtonClicked(self) -> typing.NoReturn:
        '''Manage browse for directory
        '''
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
        path = settings.value("last_file_directory", QtCore.QDir.homePath())
        dir = QtWidgets.QFileDialog.getExistingDirectory(None, "Select output directory", path)
        if dir:
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
                # self.covariatesProcesser.setBasename(self.ui.basenameLineEdit.text())
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Invalid basename")
                msgBox.setInformativeText("The basename " + self.ui.basenameLineEdit.text() + " is not valid")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                _ = msgBox.exec_()

        self.updateSaveStatus(True)
