# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        PreferencesDialog.setObjectName("PreferencesDialog")
        PreferencesDialog.setWindowModality(QtCore.Qt.WindowModal)
        PreferencesDialog.resize(718, 528)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PreferencesDialog.sizePolicy().hasHeightForWidth())
        PreferencesDialog.setSizePolicy(sizePolicy)
        PreferencesDialog.setSizeGripEnabled(False)
        PreferencesDialog.setModal(True)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(PreferencesDialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QtWidgets.QWidget(PreferencesDialog)
        self.widget.setObjectName("widget")
        self.verticalLayout_5.addWidget(self.widget)
        self.tabWidget = QtWidgets.QTabWidget(PreferencesDialog)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSearch = QtWidgets.QWidget()
        self.tabSearch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabSearch.setObjectName("tabSearch")
        self.horizontalLayout_3 = QtWidgets.QVBoxLayout(self.tabSearch)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelSearchFilerByLanguage = QtWidgets.QLabel(self.tabSearch)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSearchFilerByLanguage.sizePolicy().hasHeightForWidth())
        self.labelSearchFilerByLanguage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelSearchFilerByLanguage.setFont(font)
        self.labelSearchFilerByLanguage.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.labelSearchFilerByLanguage.setObjectName("labelSearchFilerByLanguage")
        self.horizontalLayout_3.addWidget(self.labelSearchFilerByLanguage)
        self.scrollAreaSearch = QtWidgets.QScrollArea(self.tabSearch)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaSearch.sizePolicy().hasHeightForWidth())
        self.scrollAreaSearch.setSizePolicy(sizePolicy)
        self.scrollAreaSearch.setMinimumSize(QtCore.QSize(0, 150))
        self.scrollAreaSearch.setWidgetResizable(True)
        self.scrollAreaSearch.setObjectName("scrollAreaSearch")
        self.scrollAreaWidgetSearch = QtWidgets.QWidget()
        self.scrollAreaWidgetSearch.setGeometry(QtCore.QRect(0, 0, 678, 365))
        self.scrollAreaWidgetSearch.setObjectName("scrollAreaWidgetSearch")
        self.vbox_B = QtWidgets.QVBoxLayout(self.scrollAreaWidgetSearch)
        self.vbox_B.setObjectName("vbox_B")
        self.scrollAreaWidgetLayoutSearch = QtWidgets.QGridLayout()
        self.scrollAreaWidgetLayoutSearch.setObjectName("scrollAreaWidgetLayoutSearch")
        self.vbox_B.addLayout(self.scrollAreaWidgetLayoutSearch)
        self.scrollAreaSearch.setWidget(self.scrollAreaWidgetSearch)
        self.horizontalLayout_3.addWidget(self.scrollAreaSearch)
        self.tabWidget.addTab(self.tabSearch, "")
        self.tabDownload = QtWidgets.QWidget()
        self.tabDownload.setObjectName("tabDownload")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabDownload)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.tabDownload)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_B = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_B.setObjectName("verticalLayout_B")
        self.horizontalLayout_B = QtWidgets.QHBoxLayout()
        self.horizontalLayout_B.setObjectName("horizontalLayout_B")
        self.scrollArea_B = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea_B.setWidgetResizable(True)
        self.scrollArea_B.setObjectName("scrollArea_B")
        self.scrollAreaWidgetContents_B = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_B.setGeometry(QtCore.QRect(0, 0, 656, 67))
        self.scrollAreaWidgetContents_B.setObjectName("scrollAreaWidgetContents_B")
        self.scrollArea_B.setWidget(self.scrollAreaWidgetContents_B)
        self.horizontalLayout_B.addWidget(self.scrollArea_B)
        self.verticalLayout_B.addLayout(self.horizontalLayout_B)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.optionDownloadFolderAsk = QtWidgets.QRadioButton(self.groupBox)
        self.optionDownloadFolderAsk.setObjectName("optionDownloadFolderAsk")
        self.verticalLayout_6.addWidget(self.optionDownloadFolderAsk)
        self.optionDownloadFolderSame = QtWidgets.QRadioButton(self.groupBox)
        self.optionDownloadFolderSame.setChecked(True)
        self.optionDownloadFolderSame.setObjectName("optionDownloadFolderSame")
        self.verticalLayout_6.addWidget(self.optionDownloadFolderSame)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.optionDownloadFolderPredefined = QtWidgets.QRadioButton(self.groupBox)
        self.optionDownloadFolderPredefined.setObjectName("optionDownloadFolderPredefined")
        self.horizontalLayout_6.addWidget(self.optionDownloadFolderPredefined)
        self.optionPredefinedFolderText = QtWidgets.QLineEdit(self.groupBox)
        self.optionPredefinedFolderText.setReadOnly(True)
        self.optionPredefinedFolderText.setObjectName("optionPredefinedFolderText")
        self.horizontalLayout_6.addWidget(self.optionPredefinedFolderText)
        self.optionButtonChooseFolder = QtWidgets.QPushButton(self.groupBox)
        self.optionButtonChooseFolder.setObjectName("optionButtonChooseFolder")
        self.horizontalLayout_6.addWidget(self.optionButtonChooseFolder)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.verticalLayout_B.addLayout(self.verticalLayout_6)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tabDownload)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.optionDownloadSameFilename = QtWidgets.QRadioButton(self.groupBox_2)
        self.optionDownloadSameFilename.setChecked(True)
        self.optionDownloadSameFilename.setObjectName("optionDownloadSameFilename")
        self.verticalLayout_2.addWidget(self.optionDownloadSameFilename)
        self.optionDownloadSameFilenamePlusLang = QtWidgets.QRadioButton(self.groupBox_2)
        self.optionDownloadSameFilenamePlusLang.setChecked(False)
        self.optionDownloadSameFilenamePlusLang.setObjectName("optionDownloadSameFilenamePlusLang")
        self.verticalLayout_2.addWidget(self.optionDownloadSameFilenamePlusLang)
        self.optionDownloadSameFilenamePlusLangAndUploader = QtWidgets.QRadioButton(self.groupBox_2)
        self.optionDownloadSameFilenamePlusLangAndUploader.setChecked(False)
        self.optionDownloadSameFilenamePlusLangAndUploader.setObjectName("optionDownloadSameFilenamePlusLangAndUploader")
        self.verticalLayout_2.addWidget(self.optionDownloadSameFilenamePlusLangAndUploader)
        self.optionDownloadOnlineSubName = QtWidgets.QRadioButton(self.groupBox_2)
        self.optionDownloadOnlineSubName.setObjectName("optionDownloadOnlineSubName")
        self.verticalLayout_2.addWidget(self.optionDownloadOnlineSubName)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.tabDownload, "")
        self.tabUpload = QtWidgets.QWidget()
        self.tabUpload.setObjectName("tabUpload")
        self.layoutWidget = QtWidgets.QWidget(self.tabUpload)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 521, 52))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setSpacing(8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_55 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_55.setFont(font)
        self.label_55.setObjectName("label_55")
        self.horizontalLayout_4.addWidget(self.label_55)
        self.optionDefaultUploadLanguage = QtWidgets.QComboBox(self.layoutWidget)
        self.optionDefaultUploadLanguage.setMinimumSize(QtCore.QSize(0, 20))
        self.optionDefaultUploadLanguage.setObjectName("optionDefaultUploadLanguage")
        self.horizontalLayout_4.addWidget(self.optionDefaultUploadLanguage)
        self.tabWidget.addTab(self.tabUpload, "")
        self.tabNetwork = QtWidgets.QWidget()
        self.tabNetwork.setObjectName("tabNetwork")
        self.label_52 = QtWidgets.QLabel(self.tabNetwork)
        self.label_52.setGeometry(QtCore.QRect(20, 10, 131, 18))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_52.setFont(font)
        self.label_52.setObjectName("label_52")
        self.layoutWidget1 = QtWidgets.QWidget(self.tabNetwork)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 30, 241, 80))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_60 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_60.setObjectName("label_60")
        self.gridLayout.addWidget(self.label_60, 0, 0, 1, 1)
        self.optionProxyHost = QtWidgets.QLineEdit(self.layoutWidget1)
        self.optionProxyHost.setObjectName("optionProxyHost")
        self.gridLayout.addWidget(self.optionProxyHost, 0, 1, 1, 1)
        self.label_59 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_59.setObjectName("label_59")
        self.gridLayout.addWidget(self.label_59, 1, 0, 1, 1)
        self.optionProxyPort = QtWidgets.QSpinBox(self.layoutWidget1)
        self.optionProxyPort.setMaximum(99999)
        self.optionProxyPort.setProperty("value", 8080)
        self.optionProxyPort.setObjectName("optionProxyPort")
        self.gridLayout.addWidget(self.optionProxyPort, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tabNetwork, "")
        self.tabOthers = QtWidgets.QWidget()
        self.tabOthers.setObjectName("tabOthers")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabOthers)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_61 = QtWidgets.QLabel(self.tabOthers)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_61.setFont(font)
        self.label_61.setObjectName("label_61")
        self.horizontalLayout.addWidget(self.label_61)
        self.optionInterfaceLanguage = QtWidgets.QComboBox(self.tabOthers)
        self.optionInterfaceLanguage.setObjectName("optionInterfaceLanguage")
        self.horizontalLayout.addWidget(self.optionInterfaceLanguage)
        self.helpTranslateButton = QtWidgets.QPushButton(self.tabOthers)
        self.helpTranslateButton.setObjectName("helpTranslateButton")
        self.horizontalLayout.addWidget(self.helpTranslateButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_62 = QtWidgets.QLabel(self.tabOthers)
        self.label_62.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_62.setFont(font)
        self.label_62.setObjectName("label_62")
        self.horizontalLayout_5.addWidget(self.label_62)
        self.optionIntegrationExplorer = QtWidgets.QCheckBox(self.tabOthers)
        self.optionIntegrationExplorer.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionIntegrationExplorer.sizePolicy().hasHeightForWidth())
        self.optionIntegrationExplorer.setSizePolicy(sizePolicy)
        self.optionIntegrationExplorer.setMinimumSize(QtCore.QSize(0, 22))
        self.optionIntegrationExplorer.setObjectName("optionIntegrationExplorer")
        self.horizontalLayout_5.addWidget(self.optionIntegrationExplorer)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_63 = QtWidgets.QLabel(self.tabOthers)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_63.setFont(font)
        self.label_63.setObjectName("label_63")
        self.gridLayout_4.addWidget(self.label_63, 0, 0, 1, 2)
        self.label_67 = QtWidgets.QLabel(self.tabOthers)
        self.label_67.setObjectName("label_67")
        self.gridLayout_4.addWidget(self.label_67, 1, 0, 1, 1)
        self.optionVideoAppLocation = QtWidgets.QLineEdit(self.tabOthers)
        self.optionVideoAppLocation.setObjectName("optionVideoAppLocation")
        self.gridLayout_4.addWidget(self.optionVideoAppLocation, 1, 1, 1, 1)
        self.optionVideoAppChooseLocation = QtWidgets.QPushButton(self.tabOthers)
        self.optionVideoAppChooseLocation.setObjectName("optionVideoAppChooseLocation")
        self.gridLayout_4.addWidget(self.optionVideoAppChooseLocation, 1, 2, 1, 1)
        self.label_66 = QtWidgets.QLabel(self.tabOthers)
        self.label_66.setObjectName("label_66")
        self.gridLayout_4.addWidget(self.label_66, 2, 0, 1, 1)
        self.optionVideoAppParams = QtWidgets.QLineEdit(self.tabOthers)
        self.optionVideoAppParams.setObjectName("optionVideoAppParams")
        self.gridLayout_4.addWidget(self.optionVideoAppParams, 2, 1, 1, 1)
        self.label_65 = QtWidgets.QLabel(self.tabOthers)
        self.label_65.setObjectName("label_65")
        self.gridLayout_4.addWidget(self.label_65, 3, 1, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.tabWidget.addTab(self.tabOthers, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.buttonCancel = QtWidgets.QPushButton(PreferencesDialog)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout_8.addWidget(self.buttonCancel)
        self.buttonApplyChanges = QtWidgets.QPushButton(PreferencesDialog)
        self.buttonApplyChanges.setObjectName("buttonApplyChanges")
        self.horizontalLayout_8.addWidget(self.buttonApplyChanges)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.retranslateUi(PreferencesDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesDialog)

    def retranslateUi(self, PreferencesDialog):
        _translate = QtCore.QCoreApplication.translate
        PreferencesDialog.setWindowTitle(_("Settings"))
        self.labelSearchFilerByLanguage.setText(_("Filter search results by these languages:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _("Search"))
        self.groupBox.setTitle(_("Destination folder:"))
        self.optionDownloadFolderAsk.setText(_("Always ask user"))
        self.optionDownloadFolderSame.setText(_("Same folder as video file"))
        self.optionDownloadFolderPredefined.setText(_("Predefined folder:"))
        self.optionButtonChooseFolder.setText(_("Browse..."))
        self.groupBox_2.setTitle(_("Filename of the Subtitle:"))
        self.optionDownloadSameFilename.setText(_("Same name as video file"))
        self.optionDownloadSameFilenamePlusLang.setText(_("Same name as video file + language code (ex: StarWarsCD1.eng.srt)"))
        self.optionDownloadSameFilenamePlusLangAndUploader.setText(_("Same name as video file + language code + Uploader name (ex: StarWarsCD1.eng.JohnDoe.srt)"))
        self.optionDownloadOnlineSubName.setText(_("Same name as the online subtitle"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDownload), _("Download"))
        self.label_55.setText(_("Default language of uploaded subtitles"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabUpload), _("Upload"))
        self.label_52.setText(_("Network Proxy"))
        self.label_60.setText(_("Host:"))
        self.label_59.setText(_("Port:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNetwork), _("Network"))
        self.label_61.setText(_("Interface Language:"))
        self.helpTranslateButton.setText(_("Translate This Application..."))
        self.label_62.setText(_("Context Menu:"))
        self.optionIntegrationExplorer.setText(_("Enable in your explorer"))
        self.label_63.setText(_("External application for video playback"))
        self.label_67.setText(_("Video Player:"))
        self.optionVideoAppChooseLocation.setText(_("Browse..."))
        self.label_66.setText(_("Parameters:"))
        self.label_65.setText(_("{0} = video file path; {1} = subtitle path"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOthers), _("Others"))
        self.buttonCancel.setText(_("Cancel"))
        self.buttonApplyChanges.setText(_("Save"))

from . import images_rc