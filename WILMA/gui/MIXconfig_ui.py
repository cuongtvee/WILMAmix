# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MIXconfig.ui'
#
# Created: Wed Nov 20 00:48:57 2013
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MIXconfig(object):
    def setupUi(self, MIXconfig):
        MIXconfig.setObjectName("MIXconfig")
        MIXconfig.resize(265, 334)
        MIXconfig.setWindowTitle("WILMix details")
        self.closeButtons = QtGui.QDialogButtonBox(MIXconfig)
        self.closeButtons.setGeometry(QtCore.QRect(10, 300, 191, 41))
        self.closeButtons.setOrientation(QtCore.Qt.Horizontal)
        self.closeButtons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.closeButtons.setObjectName("closeButtons")
        self.frame_proxy = QtGui.QGroupBox(MIXconfig)
        self.frame_proxy.setGeometry(QtCore.QRect(10, 10, 241, 101))
        self.frame_proxy.setObjectName("frame_proxy")
        self.proxy_recvPort = QtGui.QSpinBox(self.frame_proxy)
        self.proxy_recvPort.setGeometry(QtCore.QRect(171, 20, 60, 22))
        self.proxy_recvPort.setMaximum(65535)
        self.proxy_recvPort.setObjectName("proxy_recvPort")
        self.proxy_sendHost = QtGui.QLineEdit(self.frame_proxy)
        self.proxy_sendHost.setGeometry(QtCore.QRect(61, 70, 100, 20))
        self.proxy_sendHost.setObjectName("proxy_sendHost")
        self.proxy_sendPort = QtGui.QSpinBox(self.frame_proxy)
        self.proxy_sendPort.setGeometry(QtCore.QRect(170, 70, 60, 22))
        self.proxy_sendPort.setMaximum(65535)
        self.proxy_sendPort.setObjectName("proxy_sendPort")
        self.label_sendProcess = QtGui.QLabel(self.frame_proxy)
        self.label_sendProcess.setGeometry(QtCore.QRect(30, 50, 100, 16))
        self.label_sendProcess.setObjectName("label_sendProcess")
        self.label_recvProcess = QtGui.QLabel(self.frame_proxy)
        self.label_recvProcess.setGeometry(QtCore.QRect(30, 20, 60, 20))
        self.label_recvProcess.setObjectName("label_recvProcess")
        self.proxy_recvEnable = QtGui.QCheckBox(self.frame_proxy)
        self.proxy_recvEnable.setGeometry(QtCore.QRect(10, 20, 16, 20))
        self.proxy_recvEnable.setText("")
        self.proxy_recvEnable.setObjectName("proxy_recvEnable")
        self.proxy_sendEnable = QtGui.QCheckBox(self.frame_proxy)
        self.proxy_sendEnable.setGeometry(QtCore.QRect(10, 50, 16, 20))
        self.proxy_sendEnable.setText("")
        self.proxy_sendEnable.setObjectName("proxy_sendEnable")
        self.frame_sync = QtGui.QGroupBox(MIXconfig)
        self.frame_sync.setGeometry(QtCore.QRect(10, 120, 241, 131))
        self.frame_sync.setObjectName("frame_sync")
        self.syncButton = QtGui.QPushButton(self.frame_sync)
        self.syncButton.setGeometry(QtCore.QRect(14, 70, 211, 23))
        self.syncButton.setCheckable(True)
        self.syncButton.setObjectName("syncButton")
        self.label_sync = QtGui.QLabel(self.frame_sync)
        self.label_sync.setGeometry(QtCore.QRect(20, 40, 71, 20))
        self.label_sync.setObjectName("label_sync")
        self.label_syncTS = QtGui.QLabel(self.frame_sync)
        self.label_syncTS.setGeometry(QtCore.QRect(110, 40, 121, 20))
        self.label_syncTS.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_syncTS.setText("")
        self.label_syncTS.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_syncTS.setObjectName("label_syncTS")
        self.offsetTS = QtGui.QSpinBox(self.frame_sync)
        self.offsetTS.setGeometry(QtCore.QRect(130, 100, 91, 22))
        self.offsetTS.setMaximum(1000)
        self.offsetTS.setObjectName("offsetTS")
        self.label_offsetTS = QtGui.QLabel(self.frame_sync)
        self.label_offsetTS.setGeometry(QtCore.QRect(20, 102, 52, 21))
        self.label_offsetTS.setText("TSoffset")
        self.label_offsetTS.setWordWrap(False)
        self.label_offsetTS.setObjectName("label_offsetTS")
        self.label_TS = QtGui.QLabel(self.frame_sync)
        self.label_TS.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.label_TS.setObjectName("label_TS")
        self.label_TSvalue = QtGui.QLabel(self.frame_sync)
        self.label_TSvalue.setGeometry(QtCore.QRect(80, 20, 151, 20))
        self.label_TSvalue.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_TSvalue.setText("")
        self.label_TSvalue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_TSvalue.setObjectName("label_TSvalue")
        self.frameDebug = QtGui.QGroupBox(MIXconfig)
        self.frameDebug.setGeometry(QtCore.QRect(10, 250, 241, 50))
        self.frameDebug.setObjectName("frameDebug")
        self.debugLevel = QtGui.QComboBox(self.frameDebug)
        self.debugLevel.setGeometry(QtCore.QRect(140, 20, 90, 22))
        self.debugLevel.setObjectName("debugLevel")
        self.label_debugLevel = QtGui.QLabel(self.frameDebug)
        self.label_debugLevel.setGeometry(QtCore.QRect(10, 20, 61, 16))
        self.label_debugLevel.setObjectName("label_debugLevel")

        self.retranslateUi(MIXconfig)

    def retranslateUi(self, MIXconfig):
        self.frame_proxy.setTitle(QtGui.QApplication.translate("MIXconfig", "Proxy Process Data", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_recvPort.setToolTip(QtGui.QApplication.translate("MIXconfig", "data sent to this port is forwarded to the SMi\'s /process/", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_sendHost.setToolTip(QtGui.QApplication.translate("MIXconfig", "process-data gets forwarded to this host", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_sendPort.setToolTip(QtGui.QApplication.translate("MIXconfig", "process-data gets forwarded to this port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sendProcess.setToolTip(QtGui.QApplication.translate("MIXconfig", "UDP-server to send process-data to (via OSC)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sendProcess.setText(QtGui.QApplication.translate("MIXconfig", "process →", None, QtGui.QApplication.UnicodeUTF8))
        self.label_recvProcess.setToolTip(QtGui.QApplication.translate("MIXconfig", "UDP-port to listen for connections from OSC-client for process-control", None, QtGui.QApplication.UnicodeUTF8))
        self.label_recvProcess.setText(QtGui.QApplication.translate("MIXconfig", "process↔", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_sync.setTitle(QtGui.QApplication.translate("MIXconfig", "SyncStreams", None, QtGui.QApplication.UnicodeUTF8))
        self.syncButton.setToolTip(QtGui.QApplication.translate("MIXconfig", "in \"sync\"-mode streaming/recording is sample-synchronous", None, QtGui.QApplication.UnicodeUTF8))
        self.syncButton.setText(QtGui.QApplication.translate("MIXconfig", "Sync", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sync.setToolTip(QtGui.QApplication.translate("MIXconfig", "<html><head/><body><p>sync-state of the <span style=\" font-weight:600; font-style:italic;\">received</span> streams:<ul><li><span style=\" font-style:italic;\">freewheeling</span> (out-of-sync)</li><li>current <span style=\" font-style:italic;\">receiver-timestamp</span></li></ul></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sync.setText(QtGui.QApplication.translate("MIXconfig", "freewheeling", None, QtGui.QApplication.UnicodeUTF8))
        self.offsetTS.setToolTip(QtGui.QApplication.translate("MIXconfig", "Timestamp-offset (for RECORDing) in kSamples", None, QtGui.QApplication.UnicodeUTF8))
        self.label_TS.setText(QtGui.QApplication.translate("MIXconfig", "TimeStamp:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_TSvalue.setToolTip(QtGui.QApplication.translate("MIXconfig", "average time-stamp of all active SMi\'s", None, QtGui.QApplication.UnicodeUTF8))
        self.frameDebug.setTitle(QtGui.QApplication.translate("MIXconfig", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.debugLevel.setToolTip(QtGui.QApplication.translate("MIXconfig", "control how much debugging output is generated by WILMix", None, QtGui.QApplication.UnicodeUTF8))
        self.label_debugLevel.setText(QtGui.QApplication.translate("MIXconfig", "LogLevel", None, QtGui.QApplication.UnicodeUTF8))

