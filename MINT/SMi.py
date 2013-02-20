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

from net import Server as NetServer
from net.osc import Bundle

from Launcher import Launcher
import constants

from streaming import Server as StreamingServer
from audio import AudioMeter, AudioMixer

class State:
    def __init__(self):
        self.mixer=None
        self.gains=[]
        self.levels=[]
        self.mixer = AudioMixer()
        self.meter = AudioMeter()
        self.meter.start()

    def update(self):
        self.gains=self.mixer.gain()
        self.levels=self.meter.getLevels()

class Setting:
    def __init__(self):
        self.streamtype='rtsp'
        self.streamprofile='L16'
        self.streamchannels=4


class SMi:
    def __init__(self):
        self.state=State()
        self.setting=Setting()
        self.server = NetServer(port=constants.SM_PORT)
        self.server.add(self.ping, '/ping')
        self.server.add(self.setGain, '/gain')
        self.server.add(self.controlStream, '/stream')
        self.server.add(self.controlStreamType, '/stream/settings/type')
        self.server.add(self.controlStreamProfile, '/stream/settings/profile')
        self.server.add(self.controlStreamChannels, '/stream/settings/channels')
        self.server.add(self.dumpInfo, '/dump') ## debugging
        self.launcher=None
        self.server.add(self.launchCmd, '/launch') ## debugging
        self.mixer = self.state.mixer
        self.streamer = None

    def setGain(self, msg, src):
        if self.mixer is not None:
            gains=self.mixer.gain(msg[2:])

    def controlStreamType(self, msg, src):
        self.setting.streamtype=msg[2]

    def controlStreamProfile(self, msg, src):
        self.setting.streamprofile=msg[2]

    def controlStreamChannels(self, msg, src):
        self.setting.streamchannels=msg[2]


    def controlStream(self, msg, src):
        state=msg[2]
        #print "controlStream", msg
        if state is not None and int(state) > 0:
            self.startStream()
        else:
            self.stopStream()

    def startStream(self):
        if self.streamer is not None:
            self.stopStream()
        self.streamer = StreamingServer(type=self.setting.streamtype, profile=self.setting.streamprofile, channels=self.setting.streamchannels)
        self.streamer.start()
        self.server.sendMsg('/stream/uri', [self.streamer.getURI()])

    def stopStream(self):
        if self.streamer is not None:
            self.streamer.stop()
        self.streamer = None

    def ping(self, msg, src):
        self.state.update()
        bundle = Bundle()
        bundle.append(('/gain', self.state.gains))
        bundle.append(('/level', self.state.levels))
        bundle.append(('/launch/state', [self.launcher is not None]))
        self.server.sendBundle(bundle)

    def dumpInfo(self, msg, src):
        print "setting: ", self.setting.__dict__
        print "state  : ", self.state.__dict__
        if self.streamer is not None:
            self.streamer.dumpInfo()

    def launchCmd(self, msg, src):
        print "launching: ", msg
        if self.launcher is not None:
            return
        self.launcher = Launcher(msg[2], cwd='/tmp', doneCb=self.launchCb)
        self.launcher.start()
        self.server.sendMsg('/launch/state', [True])
    def launchCb(self):
        print "launch callback", self.server
        self.launcher = None

if __name__ == '__main__':
    print "SMi..."
    import gobject
    sm = SMi()
    import time

    try:
        gobject.MainLoop().run()
    except KeyboardInterrupt:
        pass


