## ###########################################################################
##
# mics_geocode_config_reader.py
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
class mics_geocode_config_reader:
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

			if configReader['state']['isStep1'] == "True":
				self.mainWindow.ui.tabWidget.setCurrentIndex(0)
			else:
				self.mainWindow.ui.tabWidget.setCurrentIndex(1)

			if 'global' in configReader:
				if 'basename' in configReader['global']:
					self.mainWindow.ui.basenameLineEdit.setText(configReader['global']['basename'])
					self.mainWindow.onBasenameLineEditChanged()

				if 'outputDir' in configReader['global']:
					try:
						self.mainWindow.ui.outputDirLineEdit.setText( os.path.realpath(os.path.join(project_root_path, configReader['global']['outputDir'])))
					except:
						self.mainWindow.ui.outputDirLineEdit.clear()

			if 'ReferenceLayer' in configReader:
				if 'fileReferenceLayer' in configReader['ReferenceLayer']:
					try:
						self.mainWindow.ui.referenceLayerLineEdit.setText( os.path.realpath(os.path.join(project_root_path, configReader['ReferenceLayer']['fileReferenceLayer'])))
					except:
						self.mainWindow.ui.referenceLayerLineEdit.clear()
				if 'fileReferenceLayerField' in configReader['ReferenceLayer']:
					self.mainWindow.ui.referenceLayerFieldCombobox.setCurrentIndex(int(configReader['ReferenceLayer']['fileReferenceLayerField']))
				if 'ruralTypes' in configReader['ReferenceLayer']:
					self.mainWindow.ui.ruralValuesLineEdit.setText(configReader['ReferenceLayer']['ruralTypes'])
				if 'urbanTypes' in configReader['ReferenceLayer']:
					self.mainWindow.ui.urbanValuesLineEdit.setText(configReader['ReferenceLayer']['urbanTypes'])

			if 'CentroidsSource' in configReader:
				if 'file' in configReader['CentroidsSource']:
					try:
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
		except:
			Logger.logWarn("[ConfigReader] A problem occured while loading the project from :  " + self.fileMGC)

