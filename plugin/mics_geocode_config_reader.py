import platform
import os

import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .micsgeocode.Logger import Logger
class mics_geocode_config_reader:
	## #####################################################################
	## Start, Load, Unload
	## #####################################################################
	def __init__(self, fileMGC, mainWindow):
		self.mainWindow = mainWindow
		self.fileMGC = fileMGC

	def readConfig(self):
		try:
			project_root_path = os.path.dirname(os.path.realpath(self.fileMGC))

			configReader = configparser.ConfigParser()
			configReader.read(self.fileMGC)

			if configReader['state']['isStep1'] == "True":
				self.mainWindow.ui.tabWidget.setCurrentIndex(0)
			else:
				self.mainWindow.ui.tabWidget.setCurrentIndex(1)

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
						self.mainWindow.ui.centroidsSourceFileLineEdit.setText(os.path.realpath(os.path.join(project_root_path, configReader['CentroidsSource']['file'])))
					except:
						self.mainWindow.ui.centroidsSourceFileLineEdit.clear()
				if 'stackIndex'in configReader['CentroidsSource']:
					self.mainWindow.ui.stackFields.setCurrentIndex(int(configReader['CentroidsSource']['stackIndex']))
				if 'numeroIndex' in configReader['CentroidsSource']:
					self.mainWindow.ui.numeroFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['numeroIndex']))
				if 'typeIndex' in configReader['CentroidsSource']:
					self.mainWindow.ui.typeFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['typeIndex']))
				if 'latIndex' in configReader['CentroidsSource']:
					self.mainWindow.ui.latitudeFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['latIndex']))
				if 'longIndex' in configReader['CentroidsSource']:
					self.mainWindow.ui.longitudeFieldComboBox.setCurrentIndex(int(configReader['CentroidsSource']['longIndex']))
				if 'numeroIndexLE' in configReader['CentroidsSource']:
					self.mainWindow.ui.numeroFieldLineEdit.setText(configReader['CentroidsSource']['numeroIndexLE'])
				if 'typeIndexLE' in configReader['CentroidsSource']:
					self.mainWindow.ui.typeFieldLineEdit.setText(configReader['CentroidsSource']['typeIndexLE'])
				if 'latIndexLE' in configReader['CentroidsSource']:
					self.mainWindow.ui.latitudeFieldLineEdit.setText(configReader['CentroidsSource']['latIndexLE'])
				if 'longIndexLE' in configReader['CentroidsSource']:
					self.mainWindow.ui.longitudeFieldLineEdit.setText(configReader['CentroidsSource']['longIndexLE'])
		except:
			Logger.logInfo("A problem occured while loading the project from :  " + self.fileMGC)
