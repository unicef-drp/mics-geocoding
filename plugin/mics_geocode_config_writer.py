import platform
import os
from os.path import relpath

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .micsgeocode.Logger import Logger

import configparser

class mics_geocode_config_writer:

	## #####################################################################
	## Start, Load, Unload
	## #####################################################################
	def __init__(self, fileMGC, mainWindow):
		self.mainWindow = mainWindow
		self.fileMGC = fileMGC

	def writeConfig(self):
		try:
			project_root_path = os.path.dirname(os.path.realpath(self.fileMGC))

			configWriter = configparser.ConfigParser()


			try:
				ref_file = os.path.relpath(self.mainWindow.ui.referenceLayerLineEdit.text(), project_root_path)
			except:
				ref_file = ""

			try:
				centroid_file = os.path.relpath(self.mainWindow.ui.centroidsSourceFileLineEdit.text(), project_root_path)
			except:
				centroid_file = ""

			try:
				output_dir = os.path.relpath(self.mainWindow.ui.outputDirLineEdit.text(), project_root_path)
			except:
				output_dir = ""

			configWriter['program'] = {'name' : 'MicsGeocodePlugin', 'version' : '0.0.1'}
			configWriter['state'] = {'isStep1' : (self.mainWindow.ui.tabWidget.currentIndex() == 0)}

			configWriter['global'] = {
				'basename': self.mainWindow.ui.basenameLineEdit.text(),
				'outputDir': output_dir
			}

			configWriter['ReferenceLayer'] = {
				'fileReferenceLayer': ref_file,
				'fileReferenceLayerField': str(self.mainWindow.ui.referenceLayerFieldCombobox.currentIndex()),
				'ruralTypes': self.mainWindow.ui.ruralValuesLineEdit.text(),
				'urbanTypes': self.mainWindow.ui.urbanValuesLineEdit.text()
			}
			configWriter['CentroidsSource'] = {
				'file': centroid_file,
				'stackIndex': str(self.mainWindow.ui.stackFields.currentIndex()),
				'numeroIndex': str(self.mainWindow.ui.numeroFieldComboBox.currentIndex()),
				'typeIndex': str(self.mainWindow.ui.typeFieldComboBox.currentIndex()),
				'latIndex': str(self.mainWindow.ui.latitudeFieldComboBox.currentIndex()),
				'longIndex': str(self.mainWindow.ui.longitudeFieldComboBox.currentIndex()),
				'numeroIndexLE': str(self.mainWindow.ui.numeroFieldLineEdit.text()),
				'typeIndexLE': str(self.mainWindow.ui.typeFieldLineEdit.text()),
				'latIndexLE': str(self.mainWindow.ui.latitudeFieldLineEdit.text()),
				'longIndexLE': str(self.mainWindow.ui.longitudeFieldLineEdit.text())
			}

			with open(self.fileMGC, 'w') as file:
				configWriter.write(file)
		except:
			Logger.logInfo("A problem occured while saving the project to :  " + self.fileMGC)