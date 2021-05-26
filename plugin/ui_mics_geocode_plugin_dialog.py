# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2020\MICS_geocoding\Repo\plugin\mics_geocode_plugin_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MicsGeocodePluginDialog(object):
    def setupUi(self, MicsGeocodePluginDialog):
        MicsGeocodePluginDialog.setObjectName("MicsGeocodePluginDialog")
        MicsGeocodePluginDialog.resize(505, 724)
        self.verticalLayoutWidget = QtWidgets.QWidget(MicsGeocodePluginDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 143, 481, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 400))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_step1 = QtWidgets.QWidget()
        self.tab_step1.setAutoFillBackground(False)
        self.tab_step1.setObjectName("tab_step1")
        self.groupBoxCentroid = QtWidgets.QGroupBox(self.tab_step1)
        self.groupBoxCentroid.setGeometry(QtCore.QRect(10, 10, 451, 241))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxCentroid.sizePolicy().hasHeightForWidth())
        self.groupBoxCentroid.setSizePolicy(sizePolicy)
        self.groupBoxCentroid.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxCentroid.setFlat(False)
        self.groupBoxCentroid.setObjectName("groupBoxCentroid")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBoxCentroid)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 20, 441, 211))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayoutCSF = QtWidgets.QHBoxLayout()
        self.horizontalLayoutCSF.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayoutCSF.setObjectName("horizontalLayoutCSF")
        self.centroidsSourceFileLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centroidsSourceFileLabel.sizePolicy().hasHeightForWidth())
        self.centroidsSourceFileLabel.setSizePolicy(sizePolicy)
        self.centroidsSourceFileLabel.setObjectName("centroidsSourceFileLabel")
        self.horizontalLayoutCSF.addWidget(self.centroidsSourceFileLabel)
        self.centroidsSourceFileLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.centroidsSourceFileLineEdit.setObjectName("centroidsSourceFileLineEdit")
        self.horizontalLayoutCSF.addWidget(self.centroidsSourceFileLineEdit)
        self.centroidsSourceFileToolButton = QtWidgets.QToolButton(self.verticalLayoutWidget_3)
        self.centroidsSourceFileToolButton.setObjectName("centroidsSourceFileToolButton")
        self.horizontalLayoutCSF.addWidget(self.centroidsSourceFileToolButton)
        self.verticalLayout_3.addLayout(self.horizontalLayoutCSF)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.typeFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.typeFieldLabel_2.setObjectName("typeFieldLabel_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.typeFieldLabel_2)
        self.typeFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.typeFieldComboBox.setObjectName("typeFieldComboBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.typeFieldComboBox)
        self.numeroFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.numeroFieldLabel_2.setObjectName("numeroFieldLabel_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.numeroFieldLabel_2)
        self.numeroFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.numeroFieldComboBox.setObjectName("numeroFieldComboBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.numeroFieldComboBox)
        self.longitudeFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.longitudeFieldLabel_2.setObjectName("longitudeFieldLabel_2")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.longitudeFieldLabel_2)
        self.longitudeFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.longitudeFieldComboBox.setObjectName("longitudeFieldComboBox")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.longitudeFieldComboBox)
        self.latitudeFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.latitudeFieldLabel_2.setObjectName("latitudeFieldLabel_2")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.latitudeFieldLabel_2)
        self.latitudeFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.latitudeFieldComboBox.setObjectName("latitudeFieldComboBox")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.latitudeFieldComboBox)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        self.loadCentroidsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.loadCentroidsButton.setMinimumSize(QtCore.QSize(0, 30))
        self.loadCentroidsButton.setObjectName("loadCentroidsButton")
        self.verticalLayout_3.addWidget(self.loadCentroidsButton)
        self.groupBoxDisplacer = QtWidgets.QGroupBox(self.tab_step1)
        self.groupBoxDisplacer.setGeometry(QtCore.QRect(10, 250, 451, 191))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxDisplacer.sizePolicy().hasHeightForWidth())
        self.groupBoxDisplacer.setSizePolicy(sizePolicy)
        self.groupBoxDisplacer.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxDisplacer.setObjectName("groupBoxDisplacer")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBoxDisplacer)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 23, 441, 161))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayoutRL = QtWidgets.QHBoxLayout()
        self.horizontalLayoutRL.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayoutRL.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayoutRL.setObjectName("horizontalLayoutRL")
        self.referenceLayerLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.referenceLayerLabel.sizePolicy().hasHeightForWidth())
        self.referenceLayerLabel.setSizePolicy(sizePolicy)
        self.referenceLayerLabel.setObjectName("referenceLayerLabel")
        self.horizontalLayoutRL.addWidget(self.referenceLayerLabel)
        self.referenceLayerLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.referenceLayerLineEdit.setObjectName("referenceLayerLineEdit")
        self.horizontalLayoutRL.addWidget(self.referenceLayerLineEdit)
        self.referenceLayerToolButton = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        self.referenceLayerToolButton.setObjectName("referenceLayerToolButton")
        self.horizontalLayoutRL.addWidget(self.referenceLayerToolButton)
        self.referenceLayerFieldCombobox = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.referenceLayerFieldCombobox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.referenceLayerFieldCombobox.sizePolicy().hasHeightForWidth())
        self.referenceLayerFieldCombobox.setSizePolicy(sizePolicy)
        self.referenceLayerFieldCombobox.setMinimumSize(QtCore.QSize(100, 0))
        self.referenceLayerFieldCombobox.setObjectName("referenceLayerFieldCombobox")
        self.horizontalLayoutRL.addWidget(self.referenceLayerFieldCombobox)
        self.verticalLayout_4.addLayout(self.horizontalLayoutRL)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.ruralValuesLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.ruralValuesLabel.setObjectName("ruralValuesLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ruralValuesLabel)
        self.ruralValuesLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.ruralValuesLineEdit.setInputMask("")
        self.ruralValuesLineEdit.setText("")
        self.ruralValuesLineEdit.setObjectName("ruralValuesLineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ruralValuesLineEdit)
        self.urbanValuesLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.urbanValuesLabel.setObjectName("urbanValuesLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.urbanValuesLabel)
        self.urbanValuesLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.urbanValuesLineEdit.setInputMask("")
        self.urbanValuesLineEdit.setText("")
        self.urbanValuesLineEdit.setObjectName("urbanValuesLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.urbanValuesLineEdit)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        self.displaceCentroidsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.displaceCentroidsButton.setMinimumSize(QtCore.QSize(0, 30))
        self.displaceCentroidsButton.setObjectName("displaceCentroidsButton")
        self.verticalLayout_4.addWidget(self.displaceCentroidsButton)
        self.tabWidget.addTab(self.tab_step1, "")
        self.tab_step2 = QtWidgets.QWidget()
        self.tab_step2.setObjectName("tab_step2")
        self.groupBoxCentroid_2 = QtWidgets.QGroupBox(self.tab_step2)
        self.groupBoxCentroid_2.setGeometry(QtCore.QRect(10, 10, 451, 321))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxCentroid_2.sizePolicy().hasHeightForWidth())
        self.groupBoxCentroid_2.setSizePolicy(sizePolicy)
        self.groupBoxCentroid_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxCentroid_2.setFlat(False)
        self.groupBoxCentroid_2.setObjectName("groupBoxCentroid_2")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.groupBoxCentroid_2)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 20, 451, 301))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setSpacing(7)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayoutCSF_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutCSF_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayoutCSF_2.setObjectName("horizontalLayoutCSF_2")
        self.covinputsSourceFileLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.covinputsSourceFileLabel.sizePolicy().hasHeightForWidth())
        self.covinputsSourceFileLabel.setSizePolicy(sizePolicy)
        self.covinputsSourceFileLabel.setObjectName("covinputsSourceFileLabel")
        self.horizontalLayoutCSF_2.addWidget(self.covinputsSourceFileLabel)
        self.covinputsSourceFileLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.covinputsSourceFileLineEdit.setObjectName("covinputsSourceFileLineEdit")
        self.horizontalLayoutCSF_2.addWidget(self.covinputsSourceFileLineEdit)
        self.covinputsSourceFileToolButton = QtWidgets.QToolButton(self.verticalLayoutWidget_5)
        self.covinputsSourceFileToolButton.setObjectName("covinputsSourceFileToolButton")
        self.horizontalLayoutCSF_2.addWidget(self.covinputsSourceFileToolButton)
        self.verticalLayout_5.addLayout(self.horizontalLayoutCSF_2)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.filenameFieldLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.filenameFieldLabel.setObjectName("filenameFieldLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.filenameFieldLabel)
        self.filenameFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.filenameFieldComboBox.setObjectName("filenameFieldComboBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.filenameFieldComboBox)
        self.fileformatFieldLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.fileformatFieldLabel.setObjectName("fileformatFieldLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.fileformatFieldLabel)
        self.fileformatFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.fileformatFieldComboBox.setObjectName("fileformatFieldComboBox")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fileformatFieldComboBox)
        self.sumstatFieldLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.sumstatFieldLabel.setObjectName("sumstatFieldLabel")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.sumstatFieldLabel)
        self.sumstatFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.sumstatFieldComboBox.setObjectName("sumstatFieldComboBox")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sumstatFieldComboBox)
        self.columnnameFieldLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.columnnameFieldLabel.setObjectName("columnnameFieldLabel")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.columnnameFieldLabel)
        self.columnnameFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.columnnameFieldComboBox.setObjectName("columnnameFieldComboBox")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.columnnameFieldComboBox)
        self.verticalLayout_5.addLayout(self.formLayout_4)
        self.horizontalLayoutCSF_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutCSF_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayoutCSF_3.setObjectName("horizontalLayoutCSF_3")
        self.imagesSourceFileLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imagesSourceFileLabel.sizePolicy().hasHeightForWidth())
        self.imagesSourceFileLabel.setSizePolicy(sizePolicy)
        self.imagesSourceFileLabel.setObjectName("imagesSourceFileLabel")
        self.horizontalLayoutCSF_3.addWidget(self.imagesSourceFileLabel)
        self.imagesSourceFileLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.imagesSourceFileLineEdit.setObjectName("imagesSourceFileLineEdit")
        self.horizontalLayoutCSF_3.addWidget(self.imagesSourceFileLineEdit)
        self.imagesSourceFileToolButton = QtWidgets.QToolButton(self.verticalLayoutWidget_5)
        self.imagesSourceFileToolButton.setObjectName("imagesSourceFileToolButton")
        self.horizontalLayoutCSF_3.addWidget(self.imagesSourceFileToolButton)
        self.verticalLayout_5.addLayout(self.horizontalLayoutCSF_3)
        self.horizontalLayoutRL_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutRL_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayoutRL_2.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayoutRL_2.setObjectName("horizontalLayoutRL_2")
        self.covrefLayerLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.covrefLayerLabel.sizePolicy().hasHeightForWidth())
        self.covrefLayerLabel.setSizePolicy(sizePolicy)
        self.covrefLayerLabel.setObjectName("covrefLayerLabel")
        self.horizontalLayoutRL_2.addWidget(self.covrefLayerLabel)
        self.covrefLayerLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.covrefLayerLineEdit.setObjectName("covrefLayerLineEdit")
        self.horizontalLayoutRL_2.addWidget(self.covrefLayerLineEdit)
        self.covrefLayerToolButton = QtWidgets.QToolButton(self.verticalLayoutWidget_5)
        self.covrefLayerToolButton.setObjectName("covrefLayerToolButton")
        self.horizontalLayoutRL_2.addWidget(self.covrefLayerToolButton)
        self.covrefLayerFieldCombobox = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.covrefLayerFieldCombobox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.covrefLayerFieldCombobox.sizePolicy().hasHeightForWidth())
        self.covrefLayerFieldCombobox.setSizePolicy(sizePolicy)
        self.covrefLayerFieldCombobox.setMinimumSize(QtCore.QSize(100, 0))
        self.covrefLayerFieldCombobox.setObjectName("covrefLayerFieldCombobox")
        self.horizontalLayoutRL_2.addWidget(self.covrefLayerFieldCombobox)
        self.verticalLayout_5.addLayout(self.horizontalLayoutRL_2)
        self.loadCovrefFromStep01 = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.loadCovrefFromStep01.setObjectName("loadCovrefFromStep01")
        self.verticalLayout_5.addWidget(self.loadCovrefFromStep01)
        self.computeCovariatesButton = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.computeCovariatesButton.setMinimumSize(QtCore.QSize(0, 0))
        self.computeCovariatesButton.setObjectName("computeCovariatesButton")
        self.verticalLayout_5.addWidget(self.computeCovariatesButton)
        self.label_2 = QtWidgets.QLabel(self.tab_step2)
        self.label_2.setGeometry(QtCore.QRect(10, 350, 451, 91))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.tab_step2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.layoutWidget = QtWidgets.QWidget(MicsGeocodePluginDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 660, 486, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.loadConfigButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadConfigButton.sizePolicy().hasHeightForWidth())
        self.loadConfigButton.setSizePolicy(sizePolicy)
        self.loadConfigButton.setMinimumSize(QtCore.QSize(0, 40))
        self.loadConfigButton.setObjectName("loadConfigButton")
        self.horizontalLayout_2.addWidget(self.loadConfigButton)
        self.saveConfigButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveConfigButton.sizePolicy().hasHeightForWidth())
        self.saveConfigButton.setSizePolicy(sizePolicy)
        self.saveConfigButton.setMinimumSize(QtCore.QSize(0, 40))
        self.saveConfigButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.saveConfigButton.setObjectName("saveConfigButton")
        self.horizontalLayout_2.addWidget(self.saveConfigButton)
        self.saveConfigAsButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveConfigAsButton.sizePolicy().hasHeightForWidth())
        self.saveConfigAsButton.setSizePolicy(sizePolicy)
        self.saveConfigAsButton.setMinimumSize(QtCore.QSize(0, 40))
        self.saveConfigAsButton.setObjectName("saveConfigAsButton")
        self.horizontalLayout_2.addWidget(self.saveConfigAsButton)
        self.labelLogo = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLogo.sizePolicy().hasHeightForWidth())
        self.labelLogo.setSizePolicy(sizePolicy)
        self.labelLogo.setMinimumSize(QtCore.QSize(177, 35))
        self.labelLogo.setMaximumSize(QtCore.QSize(16777215, 35))
        self.labelLogo.setText("")
        self.labelLogo.setScaledContents(True)
        self.labelLogo.setObjectName("labelLogo")
        self.horizontalLayout_2.addWidget(self.labelLogo)
        self.formLayoutWidget = QtWidgets.QWidget(MicsGeocodePluginDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 630, 481, 24))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 10, 0)
        self.formLayout.setObjectName("formLayout")
        self.configFileLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.configFileLabel.setObjectName("configFileLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.configFileLabel)
        self.configFileLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.configFileLineEdit.setEnabled(True)
        self.configFileLineEdit.setReadOnly(True)
        self.configFileLineEdit.setObjectName("configFileLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.configFileLineEdit)
        self.groupBoxOutConfig = QtWidgets.QGroupBox(MicsGeocodePluginDialog)
        self.groupBoxOutConfig.setGeometry(QtCore.QRect(10, 10, 481, 121))
        self.groupBoxOutConfig.setObjectName("groupBoxOutConfig")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBoxOutConfig)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 30, 451, 41))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.outputDirLineEdit = QtWidgets.QLineEdit(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputDirLineEdit.sizePolicy().hasHeightForWidth())
        self.outputDirLineEdit.setSizePolicy(sizePolicy)
        self.outputDirLineEdit.setText("")
        self.outputDirLineEdit.setObjectName("outputDirLineEdit")
        self.horizontalLayout_3.addWidget(self.outputDirLineEdit)
        self.outputDirToolButton = QtWidgets.QToolButton(self.layoutWidget_2)
        self.outputDirToolButton.setObjectName("outputDirToolButton")
        self.horizontalLayout_3.addWidget(self.outputDirToolButton)
        self.label_3 = QtWidgets.QLabel(self.groupBoxOutConfig)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 126, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.basenameLineEdit = QtWidgets.QLineEdit(self.groupBoxOutConfig)
        self.basenameLineEdit.setGeometry(QtCore.QRect(140, 80, 281, 22))
        self.basenameLineEdit.setText("")
        self.basenameLineEdit.setObjectName("basenameLineEdit")

        self.retranslateUi(MicsGeocodePluginDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MicsGeocodePluginDialog)

    def retranslateUi(self, MicsGeocodePluginDialog):
        _translate = QtCore.QCoreApplication.translate
        MicsGeocodePluginDialog.setWindowTitle(_translate("MicsGeocodePluginDialog", "MicsGeocodePlugin"))
        self.groupBoxCentroid.setTitle(_translate("MicsGeocodePluginDialog", "Cluster Source"))
        self.centroidsSourceFileLabel.setText(_translate("MicsGeocodePluginDialog", "Cluster Source File"))
        self.centroidsSourceFileToolButton.setText(_translate("MicsGeocodePluginDialog", "..."))
        self.typeFieldLabel_2.setText(_translate("MicsGeocodePluginDialog", "Type Field"))
        self.numeroFieldLabel_2.setText(_translate("MicsGeocodePluginDialog", "Numero Field"))
        self.longitudeFieldLabel_2.setText(_translate("MicsGeocodePluginDialog", "Longitude Field"))
        self.latitudeFieldLabel_2.setText(_translate("MicsGeocodePluginDialog", "Latitude Field"))
        self.loadCentroidsButton.setText(_translate("MicsGeocodePluginDialog", "Load Centroids"))
        self.groupBoxDisplacer.setTitle(_translate("MicsGeocodePluginDialog", "Centroid Displacement"))
        self.referenceLayerLabel.setText(_translate("MicsGeocodePluginDialog", "Reference Layer"))
        self.referenceLayerToolButton.setText(_translate("MicsGeocodePluginDialog", "..."))
        self.ruralValuesLabel.setText(_translate("MicsGeocodePluginDialog", "Rural Values"))
        self.urbanValuesLabel.setText(_translate("MicsGeocodePluginDialog", "Urban Values"))
        self.displaceCentroidsButton.setText(_translate("MicsGeocodePluginDialog", "Displace Centroids"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_step1), _translate("MicsGeocodePluginDialog", "Step 1"))
        self.groupBoxCentroid_2.setTitle(_translate("MicsGeocodePluginDialog", "Covariates inputs"))
        self.covinputsSourceFileLabel.setText(_translate("MicsGeocodePluginDialog", "Covariate input file"))
        self.covinputsSourceFileToolButton.setText(_translate("MicsGeocodePluginDialog", "..."))
        self.filenameFieldLabel.setText(_translate("MicsGeocodePluginDialog", "Filename Field"))
        self.fileformatFieldLabel.setText(_translate("MicsGeocodePluginDialog", "File Format field"))
        self.sumstatFieldLabel.setText(_translate("MicsGeocodePluginDialog", "Summary Statistic Field"))
        self.columnnameFieldLabel.setText(_translate("MicsGeocodePluginDialog", "Column Name Field"))
        self.imagesSourceFileLabel.setText(_translate("MicsGeocodePluginDialog", "Image Directory"))
        self.imagesSourceFileToolButton.setText(_translate("MicsGeocodePluginDialog", "..."))
        self.covrefLayerLabel.setText(_translate("MicsGeocodePluginDialog", "Reference Layer"))
        self.covrefLayerToolButton.setText(_translate("MicsGeocodePluginDialog", "..."))
        self.loadCovrefFromStep01.setText(_translate("MicsGeocodePluginDialog", "Load reference from Step01"))
        self.computeCovariatesButton.setText(_translate("MicsGeocodePluginDialog", "Compute covariates"))
        self.label_2.setText(_translate("MicsGeocodePluginDialog", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_step2), _translate("MicsGeocodePluginDialog", "Step 2"))
        self.loadConfigButton.setText(_translate("MicsGeocodePluginDialog", "Load"))
        self.saveConfigButton.setText(_translate("MicsGeocodePluginDialog", "Save"))
        self.saveConfigAsButton.setText(_translate("MicsGeocodePluginDialog", "Save as"))
        self.configFileLabel.setText(_translate("MicsGeocodePluginDialog", "    In-use Config File"))
        self.groupBoxOutConfig.setTitle(_translate("MicsGeocodePluginDialog", "Outputs"))
        self.label.setText(_translate("MicsGeocodePluginDialog", "Directory for outputs: "))
        self.outputDirToolButton.setText(_translate("MicsGeocodePluginDialog", "..."))
        self.label_3.setText(_translate("MicsGeocodePluginDialog", "Outputs basename:"))
