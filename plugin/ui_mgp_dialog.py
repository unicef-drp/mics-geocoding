# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Etienne\Documents\devel\unicef-mics\mics-geocoding\plugin\mgp_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MGPDialog(object):
    def setupUi(self, MGPDialog):
        MGPDialog.setObjectName("MGPDialog")
        MGPDialog.resize(509, 619)
        MGPDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.verticalLayoutWidget = QtWidgets.QWidget(MGPDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 130, 481, 391))
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
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 200))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_step1 = QtWidgets.QWidget()
        self.tab_step1.setAutoFillBackground(False)
        self.tab_step1.setObjectName("tab_step1")
        self.groupBoxCentroid = QtWidgets.QGroupBox(self.tab_step1)
        self.groupBoxCentroid.setGeometry(QtCore.QRect(10, 10, 451, 261))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxCentroid.sizePolicy().hasHeightForWidth())
        self.groupBoxCentroid.setSizePolicy(sizePolicy)
        self.groupBoxCentroid.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxCentroid.setFlat(False)
        self.groupBoxCentroid.setObjectName("groupBoxCentroid")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBoxCentroid)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 20, 441, 231))
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
        self.numeroFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.numeroFieldLabel_2.setObjectName("numeroFieldLabel_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.numeroFieldLabel_2)
        self.numeroFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.numeroFieldComboBox.setObjectName("numeroFieldComboBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.numeroFieldComboBox)
        self.typeFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.typeFieldLabel_2.setObjectName("typeFieldLabel_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.typeFieldLabel_2)
        self.typeFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.typeFieldComboBox.setObjectName("typeFieldComboBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.typeFieldComboBox)
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
        self.adminBoundariesFieldLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.adminBoundariesFieldLabel_2.setObjectName("adminBoundariesFieldLabel_2")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.adminBoundariesFieldLabel_2)
        self.adminBoundariesFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.adminBoundariesFieldComboBox.setObjectName("adminBoundariesFieldComboBox")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.adminBoundariesFieldComboBox)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.loadCentroidsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.loadCentroidsButton.setMinimumSize(QtCore.QSize(0, 30))
        self.loadCentroidsButton.setObjectName("loadCentroidsButton")
        self.verticalLayout_3.addWidget(self.loadCentroidsButton)
        self.toggleShowMoreButton = QtWidgets.QPushButton(self.tab_step1)
        self.toggleShowMoreButton.setGeometry(QtCore.QRect(10, 270, 451, 23))
        self.toggleShowMoreButton.setMaximumSize(QtCore.QSize(16777215, 25))
        self.toggleShowMoreButton.setObjectName("toggleShowMoreButton")
        self.moreWidget = QtWidgets.QWidget(self.tab_step1)
        self.moreWidget.setGeometry(QtCore.QRect(11, 297, 451, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moreWidget.sizePolicy().hasHeightForWidth())
        self.moreWidget.setSizePolicy(sizePolicy)
        self.moreWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        self.moreWidget.setObjectName("moreWidget")
        self.generateCentroidsBufferButton = QtWidgets.QPushButton(self.moreWidget)
        self.generateCentroidsBufferButton.setGeometry(QtCore.QRect(0, 4, 449, 30))
        self.generateCentroidsBufferButton.setMinimumSize(QtCore.QSize(0, 30))
        self.generateCentroidsBufferButton.setObjectName("generateCentroidsBufferButton")
        self.tabWidget.addTab(self.tab_step1, "")
        self.tab_step2 = QtWidgets.QWidget()
        self.tab_step2.setObjectName("tab_step2")
        self.groupBoxDisplacer = QtWidgets.QGroupBox(self.tab_step2)
        self.groupBoxDisplacer.setGeometry(QtCore.QRect(10, 10, 451, 231))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxDisplacer.sizePolicy().hasHeightForWidth())
        self.groupBoxDisplacer.setSizePolicy(sizePolicy)
        self.groupBoxDisplacer.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxDisplacer.setObjectName("groupBoxDisplacer")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBoxDisplacer)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 23, 441, 208))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayoutRL_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutRL_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayoutRL_3.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayoutRL_3.setObjectName("horizontalLayoutRL_3")
        self.centroidsLayerLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centroidsLayerLabel.sizePolicy().hasHeightForWidth())
        self.centroidsLayerLabel.setSizePolicy(sizePolicy)
        self.centroidsLayerLabel.setObjectName("centroidsLayerLabel")
        self.horizontalLayoutRL_3.addWidget(self.centroidsLayerLabel)
        self.centroidsLayerLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.centroidsLayerLineEdit.setObjectName("centroidsLayerLineEdit")
        self.horizontalLayoutRL_3.addWidget(self.centroidsLayerLineEdit)
        self.centroidsLayerToolButton = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        self.centroidsLayerToolButton.setObjectName("centroidsLayerToolButton")
        self.horizontalLayoutRL_3.addWidget(self.centroidsLayerToolButton)
        self.verticalLayout_4.addLayout(self.horizontalLayoutRL_3)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.centroidsLayerNumeroFieldLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.centroidsLayerNumeroFieldLabel.setObjectName("centroidsLayerNumeroFieldLabel")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.centroidsLayerNumeroFieldLabel)
        self.centroidsLayerNumeroFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.centroidsLayerNumeroFieldComboBox.setObjectName("centroidsLayerNumeroFieldComboBox")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.centroidsLayerNumeroFieldComboBox)
        self.centroidsLayerTypeFieldLabel = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.centroidsLayerTypeFieldLabel.setObjectName("centroidsLayerTypeFieldLabel")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.centroidsLayerTypeFieldLabel)
        self.centroidsLayerTypeFieldComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.centroidsLayerTypeFieldComboBox.setObjectName("centroidsLayerTypeFieldComboBox")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.centroidsLayerTypeFieldComboBox)
        self.verticalLayout_4.addLayout(self.formLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.displaceCentroidsButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.displaceCentroidsButton.setMinimumSize(QtCore.QSize(0, 30))
        self.displaceCentroidsButton.setObjectName("displaceCentroidsButton")
        self.verticalLayout_4.addWidget(self.displaceCentroidsButton)
        self.exportDisplacedCentroidsButton = QtWidgets.QPushButton(self.tab_step2)
        self.exportDisplacedCentroidsButton.setGeometry(QtCore.QRect(20, 320, 421, 30))
        self.exportDisplacedCentroidsButton.setMinimumSize(QtCore.QSize(0, 30))
        self.exportDisplacedCentroidsButton.setObjectName("exportDisplacedCentroidsButton")
        self.tabWidget.addTab(self.tab_step2, "")
        self.tab_step3 = QtWidgets.QWidget()
        self.tab_step3.setObjectName("tab_step3")
        self.groupBoxCentroid_2 = QtWidgets.QGroupBox(self.tab_step3)
        self.groupBoxCentroid_2.setGeometry(QtCore.QRect(10, 10, 451, 341))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxCentroid_2.sizePolicy().hasHeightForWidth())
        self.groupBoxCentroid_2.setSizePolicy(sizePolicy)
        self.groupBoxCentroid_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxCentroid_2.setFlat(False)
        self.groupBoxCentroid_2.setObjectName("groupBoxCentroid_2")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.groupBoxCentroid_2)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 20, 451, 311))
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
        self.formLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.formLayout_4.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_4.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
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
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
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
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
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
        self.verticalLayout_5.addLayout(self.horizontalLayoutRL_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem5)
        self.computeCovariatesButton = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.computeCovariatesButton.setMinimumSize(QtCore.QSize(0, 30))
        self.computeCovariatesButton.setObjectName("computeCovariatesButton")
        self.verticalLayout_5.addWidget(self.computeCovariatesButton)
        self.tabWidget.addTab(self.tab_step3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.layoutWidget = QtWidgets.QWidget(MGPDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 560, 486, 51))
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
        self.formLayoutWidget = QtWidgets.QWidget(MGPDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 530, 481, 24))
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
        self.groupBoxOutConfig = QtWidgets.QGroupBox(MGPDialog)
        self.groupBoxOutConfig.setGeometry(QtCore.QRect(10, 10, 481, 111))
        self.groupBoxOutConfig.setObjectName("groupBoxOutConfig")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBoxOutConfig)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 20, 451, 41))
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
        self.label_3.setGeometry(QtCore.QRect(10, 70, 101, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.basenameLineEdit = QtWidgets.QLineEdit(self.groupBoxOutConfig)
        self.basenameLineEdit.setGeometry(QtCore.QRect(125, 70, 304, 22))
        self.basenameLineEdit.setText("")
        self.basenameLineEdit.setObjectName("basenameLineEdit")

        self.retranslateUi(MGPDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MGPDialog)

    def retranslateUi(self, MGPDialog):
        _translate = QtCore.QCoreApplication.translate
        MGPDialog.setWindowTitle(_translate("MGPDialog", "MICS Geocode Plugin"))
        self.groupBoxCentroid.setTitle(_translate("MGPDialog", "Cluster Source"))
        self.centroidsSourceFileLabel.setText(_translate("MGPDialog", "Cluster Source File"))
        self.centroidsSourceFileToolButton.setText(_translate("MGPDialog", "..."))
        self.numeroFieldLabel_2.setText(_translate("MGPDialog", "Cluster Number (HH1)"))
        self.typeFieldLabel_2.setText(_translate("MGPDialog", "Area (HH6)"))
        self.longitudeFieldLabel_2.setText(_translate("MGPDialog", "Longitude"))
        self.latitudeFieldLabel_2.setText(_translate("MGPDialog", "Latitude"))
        self.adminBoundariesFieldLabel_2.setText(_translate("MGPDialog", "Admin boundaries"))
        self.loadCentroidsButton.setText(_translate("MGPDialog", "Generate Centroids"))
        self.toggleShowMoreButton.setText(_translate("MGPDialog", "Show More"))
        self.generateCentroidsBufferButton.setText(_translate("MGPDialog", "Generate Centroids Buffers"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_step1), _translate("MGPDialog", "Generate"))
        self.groupBoxDisplacer.setTitle(_translate("MGPDialog", "Centroid Displacement"))
        self.centroidsLayerLabel.setText(_translate("MGPDialog", "Centroids Source File"))
        self.centroidsLayerToolButton.setText(_translate("MGPDialog", "..."))
        self.centroidsLayerNumeroFieldLabel.setText(_translate("MGPDialog", "Cluster Number (HH1) "))
        self.centroidsLayerTypeFieldLabel.setText(_translate("MGPDialog", "Area (HH6)"))
        self.referenceLayerLabel.setText(_translate("MGPDialog", "Boundary Layer"))
        self.referenceLayerToolButton.setText(_translate("MGPDialog", "..."))
        self.displaceCentroidsButton.setText(_translate("MGPDialog", "Displace Centroids"))
        self.exportDisplacedCentroidsButton.setText(_translate("MGPDialog", "Export Displaced Centroids"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_step2), _translate("MGPDialog", "Displace"))
        self.groupBoxCentroid_2.setTitle(_translate("MGPDialog", "Covariates Input"))
        self.covinputsSourceFileLabel.setText(_translate("MGPDialog", "Covariates Input File"))
        self.covinputsSourceFileToolButton.setText(_translate("MGPDialog", "..."))
        self.filenameFieldLabel.setText(_translate("MGPDialog", "File Name"))
        self.fileformatFieldLabel.setText(_translate("MGPDialog", "File Format"))
        self.sumstatFieldLabel.setText(_translate("MGPDialog", "Summary Statistics"))
        self.columnnameFieldLabel.setText(_translate("MGPDialog", "Variable Name"))
        self.imagesSourceFileLabel.setText(_translate("MGPDialog", "Covariates input folder"))
        self.imagesSourceFileToolButton.setText(_translate("MGPDialog", "..."))
        self.covrefLayerLabel.setText(_translate("MGPDialog", "Buffer Layer"))
        self.covrefLayerToolButton.setText(_translate("MGPDialog", "..."))
        self.computeCovariatesButton.setText(_translate("MGPDialog", "Compute Covariates"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_step3), _translate("MGPDialog", "Extract"))
        self.loadConfigButton.setText(_translate("MGPDialog", "Load"))
        self.saveConfigButton.setText(_translate("MGPDialog", "Save"))
        self.saveConfigAsButton.setText(_translate("MGPDialog", "Save as"))
        self.configFileLabel.setText(_translate("MGPDialog", "    In-use Config File"))
        self.groupBoxOutConfig.setTitle(_translate("MGPDialog", "Outputs"))
        self.label.setText(_translate("MGPDialog", "Directory for outputs: "))
        self.outputDirToolButton.setText(_translate("MGPDialog", "..."))
        self.label_3.setText(_translate("MGPDialog", "Outputs basename:"))
