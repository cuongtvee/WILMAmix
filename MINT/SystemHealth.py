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

import os
import time
from threading import Thread

class SystemHealth:
    class SystemHealthThread(Thread):
        try:
            import psutil
            have_psutil = True
        except ImportError:
            have_psutil = False
            print "failed to import 'psutil'. do you have 'python-psutil' installed?"

        def __init__(self, interval=1.0, path=None):
            Thread.__init__(self)
            self.setDaemon(True)
            try:
                if path is None:
                    path='.'
                os.statvfs(path)
                self.path=path
            except None:
                self.path=os.path.expanduser('~')
            self.interval=interval
            self.cpu = 1.
            self.mem = 1.
            self.disk= 1.
            self.last=0

            self.keepRunning=True
            self.isRunning=False

        def run(self):
            if SystemHealth.SystemHealthThread.have_psutil:
                psutil=SystemHealth.SystemHealthThread.psutil
            else:
                psutil=None
            while self.keepRunning:
                self.isRunning=True
                now=time.time()

                s=os.statvfs(self.path)
                self.disk=(s.f_blocks-s.f_bfree)*1./s.f_blocks

                if psutil is not None:
                    used=psutil.used_phymem()
                    avail=psutil.avail_phymem()
                    #self.mem=psutil.phymem_usage().percent/100.
                    self.mem=(1.0*used)/(used+avail)

                    self.cpu=psutil.cpu_percent(interval=self.interval)/100.

                deltime = self.interval - (time.time()-now)
                if deltime > 0.:
                    time.sleep(deltime)
            self.isRunning=False

    def __init__(self, interval=1.0, path=None):
        self.thread = SystemHealth.SystemHealthThread(interval, path)
        self.cpu = 1.
        self.mem = 1.
        self.disk= 1.
        self.thread.start()
        while not (self.thread.keepRunning and self.thread.isRunning):
            time.sleep(0.1)
        self.update()
    def __del__(self):
        self.stop()
    def stop(self):
        if self.thread is not None:
            self.thread.keepRunning = False
            self.thread.join()
            self.thread=None
    def update(self):
        if self.thread is not None:
            self.cpu  = self.thread.cpu
            self.mem  = self.thread.mem
            self.disk = self.thread.disk
        else:
            self.cpu = 1.
            self.mem = 1.
            self.disk= 1.


######################################################################

if __name__ == '__main__':
    print "SystemHealth..."
    s=SystemHealth()
    try:
        print "CPU: ", s.cpu
        print "MEM: ", s.mem
        print "DISK: ", s.disk
        time.sleep(5)
        s.update()
        print "CPU: ", s.cpu
        print "MEM: ", s.mem
        print "DISK: ", s.disk
    except KeyboardInterrupt:
        print "shutting down"
    s.stop()
