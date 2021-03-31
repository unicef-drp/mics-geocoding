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

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .micsgeocode.Logger import Logger

import configparser

class mics_geocode_config_writer:
	'''Handle the writing of a config file
	'''
	def __init__(self, fileMGC, mainWindow):
		self.mainWindow = mainWindow
		self.fileMGC = fileMGC

	def writeConfig(self) -> typing.NoReturn:
		try:
			configWriter = configparser.ConfigParser()

			# Compute relative path
			project_root_path = os.path.dirname(os.path.realpath(self.fileMGC))
			try:
				ref_file = os.path.relpath(self.mainWindow.ui.referenceLayerLineEdit.text(), project_root_path)
			except:
				ref_file = ""

			try:
				centroid_file = os.path.relpath(self.mainWindow.ui.centroidsSourceFileLineEdit.text(), project_root_path)
			except:
				centroid_file = ""

			try:
				covinputs_file = os.path.relpath(self.mainWindow.ui.covinputsSourceFileLineEdit.text(), project_root_path)
			except:
				covinputs_file = ""

			try:
				output_dir = os.path.relpath(self.mainWindow.ui.outputDirLineEdit.text(), project_root_path)
			except:
				output_dir = ""

			try:
				images_dir = os.path.relpath(self.mainWindow.ui.imagesSourceFileLineEdit.text(), project_root_path)
			except:
				images_dir = ""

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
				'numeroIndex': str(self.mainWindow.ui.numeroFieldComboBox.currentIndex()),
				'typeIndex': str(self.mainWindow.ui.typeFieldComboBox.currentIndex()),
				'latIndex': str(self.mainWindow.ui.latitudeFieldComboBox.currentIndex()),
				'longIndex': str(self.mainWindow.ui.longitudeFieldComboBox.currentIndex()),
			}

			configWriter['CovariatesInputs'] = {
				'file': covinputs_file,
				'filenameIndex': str(self.mainWindow.ui.filenameFieldComboBox.currentIndex()),
				'fileformatIndex': str(self.mainWindow.ui.fileformatFieldComboBox.currentIndex()),
				'sumstatIndex': str(self.mainWindow.ui.sumstatFieldComboBox.currentIndex()),
				'columnnameIndex': str(self.mainWindow.ui.columnnameFieldComboBox.currentIndex()),
				'imagesDir': images_dir
			}

			with open(self.fileMGC, 'w') as file:
				configWriter.write(file)
		except:
			Logger.logWarn("[ConfigWriter] A problem occured while saving the project to :  " + self.fileMGC)