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

## that's the main instance for SMi's GUI

import configuration, filesync
from gui import SMconfig, SMchannels, ThreadedInvoke
from net import client as _NetClient
from net.osc import Bundle
import os
import datetime as _datetime

class SMgui:
    def __init__(self, mixer=None, guiparent=None, name="SMi", confs=None, maxwidth=None):
        oscprefix=name
        while oscprefix.startswith('/'):
            oscprefix=oscprefix[1:]
        interfaces=[]
        if confs is not None:
            interfaces=sorted(confs.keys())

        self.settings=configuration.getSM(name)
        self._enabled = True
        self.running=False
        self.confs=confs
        self.connection=None
        self.critical=[False]*5
        self.pingcounter=0
        self.pullCb = None
        self.pushCb = None
        self.mixer = mixer
        self.timestamp = 0
        self.oscprefix='/'+oscprefix

        try:
            defaultconf=interfaces[0]
            config = confs[defaultconf]
            self.settings['/host'] = config['address']
            self.connection = _NetClient(config['address'],
                                         config['port'],
                                         oscprefix=self.oscprefix,
                                         transport=self.settings['/protocol'])
            self._connect()
        except IndexError:
            print "no network configurations -> no connection"

        self.channels=SMchannels.SMchannels(self, guiparent=guiparent, settings=self.settings, maxwidth=maxwidth)
        self.config=SMconfig.SMconfig(self, guiparent=guiparent, settings=self.settings, interfaces=interfaces)
        self.name = name

        self.channels.launchButton.setText(self.settings['/mode'].upper())

        if confs is not None:
            print "FIXXME: confs not yet used in SMgui"

    def __del__(self):
        self.shutdown()
    def shutdown(self):
        print "shutdown", self
        self.connection.shutdown()

    def _connect(self):
        self.connection.add(self._smiUser,      '/user')
        self.connection.add(self._smiOutpath,   '/path/out')
        self.connection.add(self._smiInpath,    '/path/in')
        self.connection.add(self._smiFader,     '/gain')
        self.connection.add(self._smiLevel,     '/level')
        self.connection.add(self._smiTimestamp, '/timestamp')
        self.connection.add(self._smiStreamURI, '/stream/uri')
        self.connection.add(self._smiStateCpu,  '/state/cpu')
        self.connection.add(self._smiStateMem,  '/state/memory')
        self.connection.add(self._smiStateDisk, '/state/disk')
        self.connection.add(self._smiStateBatt, '/state/battery')
        self.connection.add(self._smiStateRuntime, '/state/runtime')

        self.connection.add(self._smiProcess, '/process/')

    def widget(self):
        return self.channels

    def select(self, value=None):
        """(de)selects this SMi, or toggles selection"""
        if value is None: ## toggle
            self._enabled = not self._enabled
        elif value:       ## selected
            self._enabled=True
        else:             ## deselected
            self._enabled=False
        self.channels.setChecked(self._enabled)
    def selected(self):
        return self._enabled and self.channels.isChecked()
    def getTimestamp(self):
        return self.timestamp

    def alive(self, isAlive=False):
        if isAlive:
            self.pingcounter=0
        else:
            self.pingcounter+=1
        if self.pingcounter >= 100:
            if self.channels.isChecked():
                self.channels.setChecked(False)
                self.config.closeButtons.setEnabled(False)
                self.config.copyConfigButton.setEnabled(False)
            if self.pingcounter > 65535:
                self.pingcounter = 100
        elif self._enabled and not self.channels.isChecked():
            self.channels.setChecked(True)
            self.config.closeButtons.setEnabled(True)
            self.config.copyConfigButton.setEnabled(True)

    def ping(self):
        self.alive()
        self.connection.sendMsg('/ping')
    def send(self, msg, data=None):
        self.connection.send(msg, data)


    ## callbacks from childs (SMchannels/SMconfig)
    def showConfig(self):
        self.config.applySettings(self.settings)
        self.config.show()

    def _hasSettingChanged(self, key, newsettings):
        if not key in newsettings:
            return False
        if (key in self.settings) and (self.settings[key]==newsettings[key]):
            return False
        self.settings[key]=newsettings[key]
        return True
    def applySettings(self, settings):
        print "FIXME: SMgui.applySettings", settings
        # /network/interface
        ## IGNORED FOR NOW
        self._hasSettingChanged('/network/interface', settings)

        # /stream
        streamchanged=(self._hasSettingChanged('/stream/protocol', settings) or
                       self._hasSettingChanged('/stream/profile' , settings) or
                       self._hasSettingChanged('/stream/channels', settings))
        # /mode
        modechanged=self._hasSettingChanged('/mode', settings)
        self.channels.launchButton.setText(self.settings['/mode'].upper())

        # if the mode has changed or the streaming settings have changed while we were streaming,
        # stop it
        if modechanged or (streamchanged and self.running and self.settings['/mode'] == 'stream'):
            self.launch(False)
        ## send new streamsettings
        props=[]
        if streamchanged:
            props += ['/stream/protocol', '/stream/profile', '/stream/channels']
        if modechanged:
            props += ['/mode']
        if len(props)>0:
            bundle = Bundle(oscprefix=self.oscprefix)
            for p in props:
                bundle.append((p, [self.settings[p]]))
            self.connection.send(bundle)

    def copySettings(self, settings):
        self.mixer.applySMiSettings(settings)
    def pull(self, path, fun=None):
        if path is None:
            return
        source=self.settings['/user']+'@'+self.settings['/host']+':'+self.settings['/path/out']+'/' #remote
        target=os.path.join(path, self.name) #local
        self.config.pullEnable(False)
        self.pullCb=fun
        f=filesync.filesync(source, target,
                            passphrases=[self.settings['/passphrase']],
                            deleteTarget=True,
                            doneCallback=ThreadedInvoke.Invoker(self.pullDone))
    def pullDone(self, state):
        self.config.pullEnable(True)
        pullCb=self.pullCb
        self.pullCb=None
        if pullCb is not None:
            pullCb(self, state)
    def push(self, path, fun=None):
        if path is None:
            return
        source=path #local
        target=self.settings['/user']+'@'+self.settings['/host']+':'+self.settings['/path/in']+'/' #remote
        self.config.pushEnable(False)
        self.pushCb=fun
        f=filesync.filesync(source, target,
                            passphrases=[self.settings['/passphrase']],
                            deleteTarget=True,
                            doneCallback=ThreadedInvoke.Invoker(self.pushDone))
    def pushDone(self, state):
        self.config.pushEnable(True)
        pushCb=self.pushCb
        self.pushCb=None
        if pushCb is not None:
            pushCb(self, state)

    def launch(self, state, ts=None):
        bundle = Bundle(oscprefix=self.oscprefix)
        mode=self.settings['/mode']
        uri ='rtp://localhost:8787' ## FIXXXXME!
        starttime=0
        if ts is not None: ## (TSmax, TSmin)
            starttime=ts[1]+10000
        bundle.append(('/record/timestamp', [starttime]))
        bundle.append(('/record/filename',  [_datetime.datetime.now().strftime('%Y%m%d-%H%M')]))
        bundle.append(('/stream/uri', [uri]))
        bundle.append(('/'+mode, [state]))
        self.running=state
        self.connection.send(bundle)

    def _smiUser(self, msg, src):
        self.settings['/user']=msg[2]
    def _smiFader(self, msg, src):
        self.config.setFader(msg[2])
    def _smiLevel(self, msg, src):
        self.alive(True)
        levels=msg[2:]
        self.channels.setLevels(levels)
        self.config.setLevels  (levels)
    def _smiTimestamp(self, msg, src):
        self.timestamp=msg[2]
        self.config.setTimestamp(self.timestamp)
    def _smiOutpath(self, msg, src):
        self.settings['/path/out']=msg[2]
    def _smiInpath (self, msg, src):
        self.settings['/path/in']=msg[2]
    def _smiStreamURI(self, msg, src):
        print "FIXME: smiURI"
    def _smiStateCpu(self, msg, src):
        value=msg[2]
        index=0
        self.config.setState(index, value)
        self.critical[index]=value>0.9
    def _smiStateMem(self, msg, src):
        value=msg[2]
        index=1
        self.config.setState(index, value)
        self.critical[index]=value>0.9
    def _smiStateDisk(self, msg, src):
        value=msg[2]
        index=2
        self.config.setState(index, value)
        self.critical[index]=value>0.9
    def _smiStateBatt(self, msg, src):
        value=msg[2]
        index=3
        self.config.setState(index, value)
        self.critical[index]=value<0.1
    def _smiStateRuntime(self, msg, src):
        value=msg[2]
        index=4
        self.config.setState(index, value)
        self.critical[index]=value<10
    def _smiProcess(self, msg, src):
        self.mixer.sendProxy(msg[0], msg[2:])
        pass


    def _proxyCallback(self, msg, src):
        if not self.selected():
            return
        addr=msg[0].split('/')
        data=msg[2:]
        addr[1]='process'
        newaddr='/'.join(addr)
        self.send(newaddr, data)

    def addProxy(self, proxy):
        subtree=self.oscprefix+'/'
        proxy.add(self._proxyCallback, subtree)


######################################################################
if __name__ == '__main__':
    import sys
    from PySide import QtGui
    class Form(QtGui.QDialog):
        def __init__(self, guiparent=None):
            super(Form, self).__init__(guiparent)
            self.d=dict()
            self.d['/network/interface']='eth0'
            self.d['/path/in' ]='/tmp/MINT/in'
            self.d['/path/out']='/tmp/MINT/out'
            self.d['/mode'    ]='stream'
            self.d['/stream/protocol']='RTP'
            self.d['/stream/profile' ]='L16'
            self.d['/stream/channels']=4
            self.d['/proxy/server/port']=9998
            self.d['/proxy/client/host']='localhost'
            self.d['/proxy/client/port']=9999
            layout = QtGui.QHBoxLayout()
            names=[]
            for i in range(10):
                names+=['SM#'+str(i)]
            self.meter=[]
            for n in names:
                m=SMgui(self, n)
                self.meter+=[m]
                layout.addWidget(m.widget())

            self.value = QtGui.QDoubleSpinBox(self)
            self.value.setMinimum(-10)
            self.value.setMaximum(120)
            layout.addWidget(self.value)
            self.setLayout(layout)
            self.value.valueChanged.connect(self.setValue)
            self.meter[0]._smiFader()
        def setValue(self, value):
            for m in self.meter:
                m.setLevels([value-100]*4)

    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
