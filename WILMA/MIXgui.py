#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2013, IOhannes m zmölnig, IEM

# This file is part of WILMix
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
# along with WILMix.  If not, see <http://www.gnu.org/licenses/>.
import logging as logging_
logging = logging_.getLogger('WILMA.MIXgui')
import sys, os.path

import metro, configuration
import SMgui
import net
from gui import SMmixer, MIXctl, MIXconfig
from gui import ThreadedInvoke

def _pdargs(settings):
    import pdsettings
    import os.path
    # first get the audio-settings from the ~/.pdsettings file
    mediasettings=pdsettings.getArgs(pdsettings.parseFile(), audio=True, midi=True, gui=False, misc=False)
    d=pdsettings.parseArgs(mediasettings)
    d=pdsettings.parseArgs(settings, d)
    argfile=os.path.join(os.path.expanduser('~'), '.config', 'wilma.iem.at', 'wilmix.pdrc')

    d=pdsettings.parseArgFile(argfile, d)
    return ['-noprefs']+pdsettings.getArgs(d)


class StreamReceiver:
    def __init__(self, parent, autostart=True):
        self.parent=None
        self.settings=None
        self.server=None
        self.receiverStateCb=None

        self.parent=parent
        self.settings=parent.settings
        self.receiverStateCb = ThreadedInvoke.Invoker(self.parent._receiverStateCb)

        pdargs=_pdargs([
                '-nogui',
                '-nrt',
                ])
        import pdserver

        self.server = pdserver.pdserver(mainpatch='_WILMAmix.pd',
                                        workingdir=self.settings['/path/out'],
                                        backend='gui',
                                        pdargs=pdargs)
        self.removeAll()
        if autostart:
            self.server.start()
    def _nullCallback(self, addr, typetags, data, source):
        pass
    def start(self):
        self.server.start()
    def stop(self):
        self.server.stop()
    def send(self, addr, data=None):
        self.server.send(addr,data)

    def removeAll(self):
        self.server.removeAll()
        self.server.add(self._nullCallback, None)
        self.server.add(self._synched, '/stream/synched')
        self.server.add(self._receiverStateCb, '/state/process')
    def add(self, callback, oscAddress):
        self.server.add(callback, oscAddress)
    def ping(self):
        self.server.ping()
    def _synched(self, addr, typetags, data, source):
        state=data[0]
        if type(state) is not int:
            state = None
        if self.parent is not None:
            self.parent._configSynched(state)
    def _receiverStateCb(self, addr, typetags, data, source):
        state=data[0]
        self.receiverStateCb(state)


class MIXgui:
    def __init__(self, parent=None):
        self.settings       = None
        self.discover       = None
        self.dict           = None
        self.pushing        = dict()
        self.pulling        = dict()
        self.proxyserver    = None
        self.proxyclient    = None
        self.mixconfig      = None
        self.mixctl         = None
        self.sm             = [] ## array of active SMi's
        self.smmixer        = None
        self.metro          = None
        self.streamreceiver = None

        self.settings=configuration.getMIX()
        for path in ['/path/out', '/path/in']:
            p=os.path.expanduser(self.settings[path])
            self.settings[path]=p

        service=(self.settings['/service']+'._'+self.settings['/protocol'])
        self.discover=net.discoverer(service=service)

        self.mixconfig = MIXconfig.MIXconfig(self, guiparent=parent, settings=self.settings)
        self.mixctl = MIXctl.MIXctl(self, guiparent=parent, settings=self.settings)
        self.smmixer=SMmixer(guiparent=parent, mixctl=self.mixctl)

        self.metro = metro.metro(self.ping, 100)

        self.streamreceiver = StreamReceiver(self, autostart=False)
        self.smmixer.show()

        self._proxyServer()
        self._proxyClient()
        self.registerProxy(self.streamreceiver)
        self.streamreceiver.start()

    def widget(self):
        return self.smmixer
    def quit(self):
        self.streamreceiver.stop()
        sys.exit(0)

    def _config(self):
        self.mixconfig.show()
    def _configSynched(self, state):
        self.mixconfig.showSync(state)
    def setSync(self, state):
        self.streamreceiver.send('/stream/sync', [state])

    def _proxyServer(self):
        self.proxyserver = None
        port=int(self.settings['/proxy/server/port'])
        if (port>0) and (port<65536):
            self.proxyserver = net.server(port=port, transport='udp', backend='gui')
            self.registerProcessProxies([self.proxyserver])
    def _proxyClient(self):
        self.proxyclient = None
        port=int(self.settings['/proxy/client/port'])
        host=self.settings['/proxy/client/host']
        if (port>0) and (port<65536):
            self.proxyclient = net.client(host=host, port=port, transport='udp', backend='gui')
            self.registerProcessProxies([self.proxyclient])
    def _nullCallback(self, addr, typetags, data, source):
        pass

    def _proxyCallback(self, addr, typetags, data, source):
        """new data from the remote add, forward it to the SMi's"""
        # FIXXME: only sent messages relevant for the given proxy
        ###  e.g.: '/SM[12]/foo/bar'
        ###  should translate to
        ###        '/SM1/process/foo/bar'
        ###        '/SM2/process/foo/bar'
        newaddr='/process'+addr[1]
        self.send(newaddr, data)
        pass

    def sendProxy(self, addr, msg=None):
        """send data to the proxy/proxies"""
        if self.proxyclient is not None:
            self.proxyclient.send(addr, msg)
        if self.proxyserver is not None:
            self.proxyserver.send(addr, msg)

    def send(self, addr, msg=None):
        """send an OSC-message to all SMi's"""
        for s in self.selected():
            s.send(addr, msg)

    def scanSM(self, doScan=True):
        self.dict = self.discover.getDict()
        for sm in self.sm:
            sm.shutdown()
        self.sm=[]

        if doScan:
            for sm in sorted(self.dict.keys()):
                d=self.dict[sm]
                smi=SMgui.SMgui(mixer=self, guiparent=self.smmixer, name=sm, netconfs=d)
                self.sm+=[smi]
        self.smmixer.setSM(self.sm)
        self.registerProcessProxies()

        self.registerProxy(self.streamreceiver)
        self.streamreceiver.send('/create', sorted(self.dict.keys()))

    def registerProcessProxies(self, proxies=None):
        """register the proxy callbacks for the various SMis"""
        if proxies is None:
            proxies = [self.proxyclient, self.proxyserver]
        for p in proxies:
            if not p:
                continue
            p.removeAll()
            for sm in self.sm:
                sm.addProcessProxy(p)
            p.add(self._nullCallback, None)
    def registerProxy(self, proxy):
        proxy.removeAll()
        for sm in self.sm:
            sm.addProxy(proxy)


    def printIt(self):
        logging.info(self.dict)

    def ping(self):
        for sm in self.sm:
            sm.ping()
        self.streamreceiver.ping()
        self.mixconfig.setTimestamps(self.getTimestamps())

    def selected(self):
        # FIXME: i'm sure this can be done very elegant with some lambda function
        result=[]
        for sm in self.sm:
            if sm.selected():
                result+=[sm]
        return result
    def select(self, state):
        for sm in self.sm:
            sm.select(state)

    def launch(self, state):
        ts=self.syncTimestamps()
        offset=0
        try:
            offset=1000*int(self.settings['/record/timestamp/offset'])
        except ValueError:
            pass
        for s in self.selected():
            s.launch(state, ts, offset)
    def pull(self, path):
        if path is None:
            self.mixctl.pushpulled(False)
            return
        self.pulling.clear()
        for s in self.selected():
            self.pulling[s]=True
            s.pull(path, self._pulled)
    def push(self, path):
        if path is None:
            self.mixctl.pushpulled(True)
            return
        self.pushing.clear()
        for s in self.selected():
            self.pushing[s]=True
            s.push(path, self._pushed)
    def _hasSettingChanged(self, key, newsettings):
        if not key in newsettings:
            return False
        if (key in self.settings) and (self.settings[key]==newsettings[key]):
            return False
        self.settings[key]=newsettings[key]
        return True
    def applySMiSettings(self, settings):
        for s in self.selected():
            s.applySettings(settings)
    def applyMixSettings(self, settings):
        proxyclientchanged = (self._hasSettingChanged('/proxy/client/port', settings) or
                              self._hasSettingChanged('/proxy/client/host', settings))
        proxyserverchanged = (self._hasSettingChanged('/proxy/server/port', settings))
        self._hasSettingChanged('/record/timestamp/offset', settings)
        if proxyclientchanged:
            self._proxyClient()
        if proxyserverchanged:
            self._proxyServer()
    def getTimestamps(self):
        ts=[]
        for s in self.selected():
            ts+=[s.getTimestamp()]
        return ts

    def syncTimestamps(self):
        ts=self.getTimestamps()
        if ts: return (max(ts), min(ts))
        return None

    def _pulled(self, sm, ret):
        self.pulling[sm]=False
        if not True in self.pulling.values():
            self.mixctl.pushpulled(False)
    def _pushed(self, sm, ret):
        self.pushing[sm]=False
        if not True in self.pushing.values():
            self.mixctl.pushpulled(True)

    def _receiverStateCb(self, state):
        if(self.mixctl.scanEnable(state)):
            self.scanSM(state)

    def proxyClientEnable(self, state):
        if self.proxyclient:
            self.proxyclient.enable(state)
    def proxyServerEnable(self, state):
        if self.proxyserver:
            self.proxyserver.enable(state)
