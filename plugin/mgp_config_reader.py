## ###########################################################################
##
# mgp_config_reader.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

import os
import typing

import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .micsgeocode.Logger import Logger


class mgp_config_reader:
    '''Handle the reading of a config file
    '''

    def __init__(self, fileMGC, mainWindow):
        self.mainWindow = mainWindow
        self.fileMGC = fileMGC

    def readConfig(self) -> typing.NoReturn:
        try:
            # Retrieve config directory - used later for absolute file path reconstruction
            project_root_path = os.path.dirname(os.path.realpath(self.fileMGC))

            configReader = configparser.ConfigParser()
            configReader.read(self.fileMGC)

            if 'global' in configReader:
                if 'basename' in configReader['global']:
                    self.mainWindow.ui.basenameLineEdit.setText(configReader['global']['basename'])
                if 'outputDir' in configReader['global']:
                    try:
                        if configReader['global']['outputDir']:
                            self.mainWindow.ui.outputDirLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['global']['outputDir'])))
                    except:
                        self.mainWindow.ui.outputDirLineEdit.clear()
                if 'tabindex' in configReader['global']:
                    self.mainWindow.ui.tabWidget.setCurrentIndex(int(configReader['global']['tabindex']))

            if 'CentroidsLayer' in configReader:
                if 'file' in configReader['CentroidsLayer']:
                    try:
                        if configReader['CentroidsLayer']['file']:
                            self.mainWindow.ui.centroidsLayerLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['CentroidsLayer']['file'])))
                    except:
                        self.mainWindow.ui.centroidsLayerLineEdit.clear()
                if 'numeroIndex' in configReader['CentroidsLayer']:
                    self.mainWindow.ui.centroidsLayerNumeroFieldComboBox.setCurrentIndex(int(configReader['CentroidsLayer']['numeroIndex']))
                if 'typeIndex' in configReader['CentroidsLayer']:
                    self.mainWindow.ui.centroidsLayerTypeFieldComboBox.setCurrentIndex(int(configReader['CentroidsLayer']['typeIndex']))
                if 'adminIndex' in configReader['CentroidsLayer']:
                    self.mainWindow.ui.centroidsLayerAdminFieldComboBox.setCurrentIndex(int(configReader['CentroidsLayer']['adminIndex']))

            if 'ReferenceLayer' in configReader:
                if 'fileReferenceLayer' in configReader['ReferenceLayer']:
                    try:
                        if configReader['ReferenceLayer']['fileReferenceLayer']:
                            self.mainWindow.ui.referenceLayerLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['ReferenceLayer']['fileReferenceLayer'])))
                    except:
                        self.mainWindow.ui.referenceLayerLineEdit.clear()
                if 'fileReferenceLayerField' in configReader['ReferenceLayer']:
                    self.mainWindow.ui.referenceLayerFieldCombobox.setCurrentIndex(int(configReader['ReferenceLayer']['fileReferenceLayerField']))

            if 'CentroidsSource' in configReader:
                if 'file' in configReader['CentroidsSource']:
                    try:
                        if configReader['CentroidsSource']['file']:
                            # Construt absolute path path from relative path
                            self.mainWindow.ui.centroidsSourceFileLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['CentroidsSource']['file'])))
                    except:
                        self.mainWindow.ui.centroidsSourceFileLineEdit.clear()
                if 'numeroIndex' in configReader['CentroidsSource']:
                    self.mainWindow.ui.numeroFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['numeroIndex']))
                if 'typeIndex' in configReader['CentroidsSource']:
                    self.mainWindow.ui.typeFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['typeIndex']))
                if 'latIndex' in configReader['CentroidsSource']:
                    self.mainWindow.ui.latitudeFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['latIndex']))
                if 'longIndex' in configReader['CentroidsSource']:
                    self.mainWindow.ui.longitudeFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['longIndex']))
                if 'adminBoundariesIndex' in configReader['CentroidsSource']:
                    self.mainWindow.ui.adminBoundariesFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['adminBoundariesIndex']))

            if 'CovariatesInputs' in configReader:
                if 'file' in configReader['CovariatesInputs']:
                    try:
                        if configReader['CovariatesInputs']['file']:
                            # Construt absolute path path from relative path
                            self.mainWindow.ui.covinputsSourceFileLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['CovariatesInputs']['file'])))
                    except:
                        self.mainWindow.ui.covinputsSourceFileLineEdit.clear()
                if 'filenameIndex' in configReader['CovariatesInputs']:
                    self.mainWindow.ui.filenameFieldComboBox.setCurrentIndex(int(configReader['CovariatesInputs']['filenameIndex']))
                if 'fileformatIndex' in configReader['CovariatesInputs']:
                    self.mainWindow.ui.fileformatFieldComboBox.setCurrentIndex(int(configReader['CovariatesInputs']['fileformatIndex']))
                if 'sumstatIndex' in configReader['CovariatesInputs']:
                    self.mainWindow.ui.sumstatFieldComboBox.setCurrentIndex(int(configReader['CovariatesInputs']['sumstatIndex']))
                if 'columnnameIndex' in configReader['CovariatesInputs']:
                    self.mainWindow.ui.columnnameFieldComboBox.setCurrentIndex(int(configReader['CovariatesInputs']['columnnameIndex']))
                if 'imagesDir' in configReader['CovariatesInputs']:
                    try:
                        if configReader['CovariatesInputs']['imagesDir']:
                            self.mainWindow.ui.imagesSourceFileLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['CovariatesInputs']['imagesDir'])))
                    except:
                        self.mainWindow.ui.imagesSourceFileLineEdit.clear()
                if 'buffer' in configReader['CovariatesInputs']:
                    try:
                        if configReader['CovariatesInputs']['buffer']:
                            self.mainWindow.ui.covrefLayerLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['CovariatesInputs']['buffer'])))
                    except:
                        self.mainWindow.ui.covrefLayerLineEdit.clear()
        except BaseException as e:
            Logger.logException("[ConfigReader] A problem occured while loading the project from :  " + self.fileMGC, e)
