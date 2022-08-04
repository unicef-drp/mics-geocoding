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


class MGPMainWindow(QtWidgets.QWidget):
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
        self.ui = Ui_MGPDialog()
        self.ui.setupUi(self)

        # Initiate ui properties
        self.setFixedSize(self.width(), self.height())
        self.title = self.windowTitle() + " (" + version + ")"
        self.setWindowTitle(self.title)

        # Down-right logo. Here file szes and label sizes are the same, no need for scaling
        # Label size: 177 x 35
        # Could be more flexible, with an horizontal spacer or halignment settings.
        # But this level of complexity was not needed at that the time.
        pixmap = QtGui.QPixmap(":/plugins/MGP/logo_wo-unicef.png")
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
        self.fileMGC = None

        # Initiate Managers

        # Hold the basename values. Made to avoid too many 'editingFinished' signal issue
        self.basename = ""
        self.ui.basenameLineEdit.clear()

        # Init output directory with tmpPath
        self.ui.outputDirLineEdit.setText(QtCore.QDir.toNativeSeparators(QtCore.QDir.tempPath()))

        # Force tab to init at first tab. Frequent mistake when manipulating qtdesigner
        self.ui.tabWidget.setCurrentIndex(0)

        self.loadCentroidsHandler = MGPMainWindowTab1Handler(self.ui)
        self.displaceCentroidsHandler = MGPMainWindowTab2Handler(self.ui)
        self.covariatesHandler = MGPMainWindowTab3Handler(self.ui)

        # Auto update output directory with default values
        self.onOutputDirLineEditChanged()

        ## ####################################################################
        # Init signal slots connection
        ## ####################################################################

        self.ui.basenameLineEdit.editingFinished.connect(self.onBasenameLineEditChanged)
        self.ui.outputDirToolButton.clicked.connect(self.onOutputDirToolButtonClicked)
        self.ui.outputDirLineEdit.textChanged.connect(self.onOutputDirLineEditChanged)

        self.ui.loadConfigButton.clicked.connect(self.onLoadConfigButtonClicked)
        self.ui.saveConfigAsButton.clicked.connect(self.onSaveConfigAsButtonClicked)
        self.ui.saveConfigButton.clicked.connect(self.onSaveConfigButtonClicked)

        ## ####################################################################
        # Init Tooltips - easier than in qtdesigner
        ## ####################################################################

        self.ui.basenameLineEdit.setToolTip("Basename of layers and file generation. Only alphanumerical characters.")

        self.ui.outputDirLineEdit.setToolTip("Output directory for shapefiles generation")
        self.ui.outputDirToolButton.setToolTip("Browse for output directory on the disk")

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
        settings = QtCore.QSettings('MICS Geocode', 'qgis plugin')
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
        reader = mgp_config_reader(self.fileMGC, self)
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
            writer = mgp_config_writer(self.fileMGC, self)
            writer.writeConfig()
            self.updateSaveStatus(False)

    def onSaveConfigAsButtonClicked(self):
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
                self.updateSaveStatus(True)
            else:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setText("Invalid basename")
                msgBox.setInformativeText("The basename " + self.ui.basenameLineEdit.text() + " is not valid.")
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
                _ = msgBox.exec_()
