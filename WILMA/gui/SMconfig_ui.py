# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SMconfig.ui'
#
# Created: Tue Oct 22 13:28:26 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SMconfig(object):
    def setupUi(self, SMconfig):
        SMconfig.setObjectName("SMconfig")
        SMconfig.resize(571, 345)
        SMconfig.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SMconfig)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frameConfig = QtGui.QWidget(SMconfig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameConfig.sizePolicy().hasHeightForWidth())
        self.frameConfig.setSizePolicy(sizePolicy)
        self.frameConfig.setAutoFillBackground(False)
        self.frameConfig.setObjectName("frameConfig")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frameConfig)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frameAudio = QtGui.QGroupBox(self.frameConfig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameAudio.sizePolicy().hasHeightForWidth())
        self.frameAudio.setSizePolicy(sizePolicy)
        self.frameAudio.setMinimumSize(QtCore.QSize(150, 0))
        self.frameAudio.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frameAudio.setObjectName("frameAudio")
        self.gainFader = QtGui.QSlider(self.frameAudio)
        self.gainFader.setGeometry(QtCore.QRect(10, 20, 16, 251))
        self.gainFader.setOrientation(QtCore.Qt.Vertical)
        self.gainFader.setObjectName("gainFader")
        self.meter = qsynthMeter(self.frameAudio)
        self.meter.setGeometry(QtCore.QRect(30, 20, 101, 251))
        self.meter.setObjectName("meter")
        self.horizontalLayout_3.addWidget(self.frameAudio)
        self.frameMid = QtGui.QWidget(self.frameConfig)
        self.frameMid.setMinimumSize(QtCore.QSize(213, 0))
        self.frameMid.setMaximumSize(QtCore.QSize(213, 16777215))
        self.frameMid.setObjectName("frameMid")
        self.frameNetwork = QtGui.QGroupBox(self.frameMid)
        self.frameNetwork.setGeometry(QtCore.QRect(1, 0, 210, 51))
        self.frameNetwork.setMinimumSize(QtCore.QSize(210, 0))
        self.frameNetwork.setObjectName("frameNetwork")
        self.networkInterface = QtGui.QComboBox(self.frameNetwork)
        self.networkInterface.setEnabled(True)
        self.networkInterface.setGeometry(QtCore.QRect(90, 20, 101, 22))
        self.networkInterface.setEditable(False)
        self.networkInterface.setObjectName("networkInterface")
        self.networkInterface.addItem("")
        self.label_networkInterface = QtGui.QLabel(self.frameNetwork)
        self.label_networkInterface.setGeometry(QtCore.QRect(10, 20, 52, 13))
        self.label_networkInterface.setObjectName("label_networkInterface")
        self.frameState = QtGui.QGroupBox(self.frameMid)
        self.frameState.setGeometry(QtCore.QRect(1, 50, 210, 141))
        self.frameState.setMinimumSize(QtCore.QSize(210, 0))
        self.frameState.setObjectName("frameState")
        self.verticalLayout = QtGui.QVBoxLayout(self.frameState)
        self.verticalLayout.setObjectName("verticalLayout")
        self.statemeter = statemeter(self.frameState)
        self.statemeter.setObjectName("statemeter")
        self.verticalLayout.addWidget(self.statemeter)
        self.frameSync = QtGui.QWidget(self.frameState)
        self.frameSync.setObjectName("frameSync")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frameSync)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stateSyncExt = QtGui.QCheckBox(self.frameSync)
        self.stateSyncExt.setEnabled(False)
        self.stateSyncExt.setCheckable(True)
        self.stateSyncExt.setChecked(False)
        self.stateSyncExt.setObjectName("stateSyncExt")
        self.horizontalLayout.addWidget(self.stateSyncExt)
        self.stateSyncInt = QtGui.QCheckBox(self.frameSync)
        self.stateSyncInt.setEnabled(False)
        self.stateSyncInt.setCheckable(True)
        self.stateSyncInt.setObjectName("stateSyncInt")
        self.horizontalLayout.addWidget(self.stateSyncInt)
        self.verticalLayout.addWidget(self.frameSync)
        self.frameTimestamp = QtGui.QWidget(self.frameState)
        self.frameTimestamp.setObjectName("frameTimestamp")
        self.gridLayout = QtGui.QGridLayout(self.frameTimestamp)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_timestamp = QtGui.QLabel(self.frameTimestamp)
        self.label_timestamp.setObjectName("label_timestamp")
        self.gridLayout.addWidget(self.label_timestamp, 0, 0, 1, 1)
        self.timestamp = QtGui.QLineEdit(self.frameTimestamp)
        self.timestamp.setFrame(True)
        self.timestamp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timestamp.setReadOnly(True)
        self.timestamp.setPlaceholderText("")
        self.timestamp.setObjectName("timestamp")
        self.gridLayout.addWidget(self.timestamp, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frameTimestamp)
        self.frameFileSync = QtGui.QGroupBox(self.frameMid)
        self.frameFileSync.setGeometry(QtCore.QRect(1, 190, 210, 91))
        self.frameFileSync.setMinimumSize(QtCore.QSize(210, 90))
        self.frameFileSync.setObjectName("frameFileSync")
        self.pullButton = QtGui.QCommandLinkButton(self.frameFileSync)
        self.pullButton.setGeometry(QtCore.QRect(10, 20, 181, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pullButton.sizePolicy().hasHeightForWidth())
        self.pullButton.setSizePolicy(sizePolicy)
        self.pullButton.setObjectName("pullButton")
        self.pushButton = QtGui.QCommandLinkButton(self.frameFileSync)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(10, 50, 181, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.frameMid)
        self.frameMode = QtGui.QWidget(self.frameConfig)
        self.frameMode.setMinimumSize(QtCore.QSize(190, 0))
        self.frameMode.setMaximumSize(QtCore.QSize(190, 16777215))
        self.frameMode.setObjectName("frameMode")
        self.frameStreamSettings = QtGui.QGroupBox(self.frameMode)
        self.frameStreamSettings.setGeometry(QtCore.QRect(0, 50, 191, 121))
        self.frameStreamSettings.setObjectName("frameStreamSettings")
        self.streamProtocol = QtGui.QComboBox(self.frameStreamSettings)
        self.streamProtocol.setGeometry(QtCore.QRect(100, 20, 81, 22))
        self.streamProtocol.setObjectName("streamProtocol")
        self.streamProtocol.addItem("")
        self.label_streamProtocol = QtGui.QLabel(self.frameStreamSettings)
        self.label_streamProtocol.setGeometry(QtCore.QRect(10, 20, 52, 22))
        self.label_streamProtocol.setObjectName("label_streamProtocol")
        self.label_streamProfile = QtGui.QLabel(self.frameStreamSettings)
        self.label_streamProfile.setGeometry(QtCore.QRect(10, 50, 52, 22))
        self.label_streamProfile.setObjectName("label_streamProfile")
        self.label_streamChannels = QtGui.QLabel(self.frameStreamSettings)
        self.label_streamChannels.setGeometry(QtCore.QRect(10, 80, 52, 22))
        self.label_streamChannels.setObjectName("label_streamChannels")
        self.streamChannels = QtGui.QSpinBox(self.frameStreamSettings)
        self.streamChannels.setGeometry(QtCore.QRect(130, 80, 50, 22))
        self.streamChannels.setMinimum(4)
        self.streamChannels.setMaximum(4)
        self.streamChannels.setObjectName("streamChannels")
        self.streamProfile = QtGui.QComboBox(self.frameStreamSettings)
        self.streamProfile.setGeometry(QtCore.QRect(100, 50, 81, 22))
        self.streamProfile.setObjectName("streamProfile")
        self.streamProfile.addItem("")
        self.frameDebug = QtGui.QGroupBox(self.frameMode)
        self.frameDebug.setGeometry(QtCore.QRect(0, 170, 191, 50))
        self.frameDebug.setObjectName("frameDebug")
        self.debugLevel = QtGui.QComboBox(self.frameDebug)
        self.debugLevel.setGeometry(QtCore.QRect(90, 20, 91, 22))
        self.debugLevel.setObjectName("debugLevel")
        self.label_debugLevel = QtGui.QLabel(self.frameDebug)
        self.label_debugLevel.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.label_debugLevel.setObjectName("label_debugLevel")
        self.frameWILMA = QtGui.QGroupBox(self.frameMode)
        self.frameWILMA.setGeometry(QtCore.QRect(0, 240, 191, 41))
        self.frameWILMA.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frameWILMA.setObjectName("frameWILMA")
        self.label_versionLabel = QtGui.QLabel(self.frameWILMA)
        self.label_versionLabel.setGeometry(QtCore.QRect(10, 15, 52, 20))
        self.label_versionLabel.setObjectName("label_versionLabel")
        self.label_version = QtGui.QLabel(self.frameWILMA)
        self.label_version.setGeometry(QtCore.QRect(60, 15, 121, 20))
        self.label_version.setText("")
        self.label_version.setObjectName("label_version")
        self.frameMode_2 = QtGui.QGroupBox(self.frameMode)
        self.frameMode_2.setGeometry(QtCore.QRect(0, 0, 191, 51))
        self.frameMode_2.setObjectName("frameMode_2")
        self.modeSelector = QtGui.QComboBox(self.frameMode_2)
        self.modeSelector.setGeometry(QtCore.QRect(40, 20, 110, 22))
        self.modeSelector.setObjectName("modeSelector")
        self.modeSelector.addItem("")
        self.modeSelector.addItem("")
        self.modeSelector.addItem("")
        self.horizontalLayout_3.addWidget(self.frameMode)
        self.verticalLayout_2.addWidget(self.frameConfig)
        self.frameButtons = QtGui.QWidget(SMconfig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameButtons.sizePolicy().hasHeightForWidth())
        self.frameButtons.setSizePolicy(sizePolicy)
        self.frameButtons.setObjectName("frameButtons")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frameButtons)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.copyConfigButton = QtGui.QPushButton(self.frameButtons)
        self.copyConfigButton.setObjectName("copyConfigButton")
        self.horizontalLayout_2.addWidget(self.copyConfigButton)
        spacerItem = QtGui.QSpacerItem(200, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.closeButtons = QtGui.QDialogButtonBox(self.frameButtons)
        self.closeButtons.setOrientation(QtCore.Qt.Horizontal)
        self.closeButtons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.closeButtons.setObjectName("closeButtons")
        self.horizontalLayout_2.addWidget(self.closeButtons)
        self.verticalLayout_2.addWidget(self.frameButtons)

        self.retranslateUi(SMconfig)

    def retranslateUi(self, SMconfig):
        SMconfig.setWindowTitle(QtGui.QApplication.translate("SMconfig", "Configuration of ...", None, QtGui.QApplication.UnicodeUTF8))
        self.frameAudio.setTitle(QtGui.QApplication.translate("SMconfig", "Audio", None, QtGui.QApplication.UnicodeUTF8))
        self.frameNetwork.setTitle(QtGui.QApplication.translate("SMconfig", "Network", None, QtGui.QApplication.UnicodeUTF8))
        self.networkInterface.setItemText(0, QtGui.QApplication.translate("SMconfig", "auto", None, QtGui.QApplication.UnicodeUTF8))
        self.label_networkInterface.setText(QtGui.QApplication.translate("SMconfig", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.frameState.setTitle(QtGui.QApplication.translate("SMconfig", "System Health", None, QtGui.QApplication.UnicodeUTF8))
        self.stateSyncExt.setText(QtGui.QApplication.translate("SMconfig", "Sync(Ext)", None, QtGui.QApplication.UnicodeUTF8))
        self.stateSyncInt.setText(QtGui.QApplication.translate("SMconfig", "Sync(Int)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_timestamp.setText(QtGui.QApplication.translate("SMconfig", "TimeStamp", None, QtGui.QApplication.UnicodeUTF8))
        self.frameFileSync.setTitle(QtGui.QApplication.translate("SMconfig", "FileSync", None, QtGui.QApplication.UnicodeUTF8))
        self.pullButton.setText(QtGui.QApplication.translate("SMconfig", "Pull data from SMi", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("SMconfig", "Push data to SMi", None, QtGui.QApplication.UnicodeUTF8))
        self.frameStreamSettings.setTitle(QtGui.QApplication.translate("SMconfig", "Stream Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.streamProtocol.setItemText(0, QtGui.QApplication.translate("SMconfig", "RTP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_streamProtocol.setText(QtGui.QApplication.translate("SMconfig", "Protocol", None, QtGui.QApplication.UnicodeUTF8))
        self.label_streamProfile.setText(QtGui.QApplication.translate("SMconfig", "Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.label_streamChannels.setText(QtGui.QApplication.translate("SMconfig", "Channels", None, QtGui.QApplication.UnicodeUTF8))
        self.streamProfile.setItemText(0, QtGui.QApplication.translate("SMconfig", "L16", None, QtGui.QApplication.UnicodeUTF8))
        self.frameDebug.setTitle(QtGui.QApplication.translate("SMconfig", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.label_debugLevel.setText(QtGui.QApplication.translate("SMconfig", "LogLevel", None, QtGui.QApplication.UnicodeUTF8))
        self.frameWILMA.setTitle(QtGui.QApplication.translate("SMconfig", "WILMA", None, QtGui.QApplication.UnicodeUTF8))
        self.label_versionLabel.setText(QtGui.QApplication.translate("SMconfig", "version:", None, QtGui.QApplication.UnicodeUTF8))
        self.frameMode_2.setTitle(QtGui.QApplication.translate("SMconfig", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.modeSelector.setItemText(0, QtGui.QApplication.translate("SMconfig", "Streaming", None, QtGui.QApplication.UnicodeUTF8))
        self.modeSelector.setItemText(1, QtGui.QApplication.translate("SMconfig", "Recording", None, QtGui.QApplication.UnicodeUTF8))
        self.modeSelector.setItemText(2, QtGui.QApplication.translate("SMconfig", "Processing", None, QtGui.QApplication.UnicodeUTF8))
        self.copyConfigButton.setText(QtGui.QApplication.translate("SMconfig", "Copy to selected SMi\'s", None, QtGui.QApplication.UnicodeUTF8))

from qsynthMeter import qsynthMeter
from statemeter import statemeter
