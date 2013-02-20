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

import osc
import socket, gobject
from Discovery import Publisher

class ServerUDP:
    """ OSC-server running on SMi.
    publishes connection information (via zeroconf),
    receives OSC-messages (and emits signals with the data),
    sends back OSC-messages
    """

    def __init__(self, host='', port=0, oscprefix=None, service=None, verbose=False):
        """creates a listener on any (or specified) port"""
        self.verbose=verbose
        self.keepListening=True
        self.oscPrefix=oscprefix

        self.remote = None
        self.addressManager = osc.CallbackManager(verbose=verbose)
        publishname=oscprefix
        if publishname is not None:
            while publishname.startswith('/'):
                publishname=publishname[1:]

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        ip, port = self.socket.getsockname()
        gobject.io_add_watch(self.socket, gobject.IO_IN, self._callback)
        if service is not None:
            self.publisher = Publisher(port=port, name=publishname, service=service+'._udp')

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.keepListening=False
        if self.socket is not None:
            try:
                self.socket.shutdown()
                self.socket.close()
            except:
                pass
        if self.publisher is not None:
            self.publisher.shutdown()
            del self.publisher
            self.publisher = None
        if self.addressManager is not None:
            del self.addressManager
            self.addressManager = None
        self.remote = None
        self.socket = None


    def _callback(self, socket, *args):
        '''Asynchronous connection listener. Starts a handler for each connection.'''
        # sock == self.socket
        data, address = socket.recvfrom(8192)
        if self.keepListening and (self.addressManager is not None):
            #self.socket = socket
            self.remote = address
            self.addressManager.handle(data, address)

        return self.keepListening

    def add(self, callback, oscAddress):
        """add a callback for oscAddress"""
        if self.addressManager is not None:
            self.addressManager.add(callback, self.oscPrefix+oscAddress)

    def _send(self, data):
        if self.socket is not None and self.remote is not None:
            if self.verbose:
                print "sending '", data, "' to ", self.remote
            self.socket.sendto( data,  self.remote)

    def sendMsg(self, oscAddress, dataArray=[]):
        """send an OSC-message to connected client(s)"""
        self._send(osc.createBinaryMsg(self.oscPrefix+oscAddress, dataArray))


    def sendBundle(self, bundle):
        """send an OSC-bundle to connected client(s)"""
        if self.socket is not None and self.remote is not None:
            if isinstance(bundle, osc.Bundle):
                self._send(bundle.data())
            else:
                self._send(bundle.message)




######################################################################

def _callback(message, source):
    print "callback (no class): ", message

class _TestServer:
    def __init__(self, port=0):
        self.serv = ServerUDP(port=port)
        self.serv.add(self.callback, '/test')

    def __del__(self):
        if self.serv is not None:
            self.serv.shutdown()
            del self.serv
            self.serv = None

    def callback(self, message, source):
        print "callback: ",message
        self.serv.sendMsg(message[0], message[2:])

    def shutdown(self):
        self.serv.shutdown()

if __name__ == '__main__':
    n = _TestServer(port=7777)

    try:
        gobject.MainLoop().run()
    except KeyboardInterrupt:
        pass
    print n
    if n is not None:
        n.shutdown()
        del n
    print "bye"
