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



################################################################
##import pyalsa.alsahcontrol as alsahcontrol
##hctl = alsahcontrol.HControl()
###hctl.list()
###element = alsahcontrol.Element(hctl,(4, 2, 0, 0, 'Amp Capture Volume', 0))
##element = alsahcontrol.Element(hctl,4)
##info = alsahcontrol.Info(element)

##value = alsahcontrol.Value(element)

##value.read()
##values = value.get_tuple(info.type, info.count)


##value.set_tuple(info.type, (10,))
##value.write()
################################################################


import alsaaudio

class AudioMixer:
    def __init__(self):
        try:
            self.mixer=alsaaudio.Mixer('Amp')
        except alsaaudio.ALSAAudioError:
            self.mixer=alsaaudio.Mixer()

    def gain(self, value=None):
        if value is not None:
            for i,v in enumerate(value):
                self.mixer.setvolume(v, i)
        gains = self.mixer.getvolume()
        gainsi = [int(i) for i in gains]
        return  gainsi


if __name__ == '__main__':
    print "SM..."
    sm = MINTsm()
    import time
    
    main_loop = gobject.MainLoop()
    print "start loop"
    try:
        main_loop.run()
    except KeyboardInterrupt:
        pass


