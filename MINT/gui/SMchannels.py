#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2013, IOhannes m zmölnig, IEM

# This file is part of MINTmix
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MINTmix.  If not, see <http://www.gnu.org/licenses/>.

from PySide import QtCore, QtGui

from qsynthMeter import qsynthMeter
from PySide.QtGui import *

class SMchannels(QtGui.QGroupBox):
    def __init__(self, parent=None, name="SMi", maxwidth=None, confs=None):
        super(SMchannels, self).__init__(parent)
        self.name = name
        self.maxWidth=maxwidth
        if confs is not None:
            print "FIXXME: confs not used in SMchannels"

        self.setTitle(self.name)
        self.setCheckable(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(2,2,2,2)

        # Create widgets
        #self.selector = QtGui.QCheckBox(self.name, self)
        #self.selector.stateChanged.connect(self.select)
        #layout.addWidget(self.selector)

        mixframe=QtGui.QFrame(self)
        sublayout=QHBoxLayout()
        sublayout.setContentsMargins(0,0,0,0)
        mixframe.setLayout(sublayout)
        layout.addWidget(mixframe)

        self.meter = qsynthMeter(self, 4, [], maxwidth=self.maxWidth) # maxwidth should be dynamic and ack the fader width
        sublayout.addWidget(self.meter)

        ## ideally the launchButton would also have
        self.launchButton = QtGui.QPushButton("START") # should be "RECORD", "STREAM" or "PROCESS"
        self.launchButton.setCheckable(True)           # so the button stays clicked (even when window is left)
        self.launchButton.clicked.connect(self.launchB)
        layout.addWidget(self.launchButton)


        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred))

    def select(self, value=None):
        """(de)selects this SMi, or toggles selection"""
        if value is None: ## toggle
            pass
        elif value:       ## selected
            pass
        else:             ## deselected
            pass
    def selected(self):
        print "FIXME: current selection state"
        pass

    def _launch(self, state): ## start launch
        """start/stop the engine on the remote SMi"""
        self.setChecked(state)
        self.launched(state) ## reflect new launch state
    def launched(self, state):
        """called from outside to set/get the current state.
        MUST NOT call launch again (but should update GUI if needed)"""
        if state is not None:
            self.launchButton.setChecked(state)
        return self.launchButton.isChecked()
    def launchB(self): ## launchButton callback, toggles the launch state
        self._launch(self.launchButton.isChecked())
        pass
    
    def setLevels(self, levels_dB=[-100.,-100.,-100.,-100.]):
        self.meter.setValues(levels_dB)

    def setState(self, level, msg):
        ## FIXME: add a status widget
        ## that gets green/red and displays the error as tooltip
        pass



    def ping(self):
        ## FIXME: compat implementation for SM.px
        pass


######################################################################
if __name__ == '__main__':
    import sys
    class Form(QtGui.QDialog):
        def __init__(self, parent=None):
            super(Form, self).__init__(parent)
            layout = QtGui.QHBoxLayout()
            names=[]
            for i in range(10):
                names+=['SM#'+str(i)]
            self.meter=[]
            for n in names:
                m=SMchannels(self, n)
                self.meter+=[m]
                layout.addWidget(m)

            self.value = QtGui.QDoubleSpinBox(self)
            self.value.setMinimum(-10)
            self.value.setMaximum(120)
            layout.addWidget(self.value)
            self.setLayout(layout)
            self.value.valueChanged.connect(self.setValue)
        def setValue(self, value):
            for m in self.meter:
                m.setLevels([value-100]*4)

    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())