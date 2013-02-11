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
import socket
from Discovery import Publisher
from threading import Thread
import SocketServer

# global dict to get the associated server in the callback
_serverdict = dict()

class _UDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        self.server.netserver._callback(socket, self.client_address, data)
##        print "{} wrote:".format(self.client_address[0])
##        print data
##        socket.sendto(data.upper(), self.client_address)

class _ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class _ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class NetServer:
    """ OSC-server running on SMi.
    publishes connection information (via zeroconf),
    receives OSC-messages (and emits signals with the data),
    sends back OSC-messages
    """
    def __init__(self, host='', port=0):
        """creates a listener on any (or specified) port"""
        self.server = _ThreadedUDPServer((host, port), _UDPHandler)
        self.server.netserver = self

        self.socket = None
        self.client = None

        ip, port = self.server.server_address
        # more thread for each request
        server_thread = Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        self.addressManager = osc.CallbackManager()
        self.publisher = Publisher(port=port)

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        if self.publisher is not None:
            self.publisher.shutdown()
            del self.publisher
            self.publisher = None
        if self.server is not None:
            self.server.shutdown()
            del self.server
            self.server = None
        if self.addressManager is not None:
            del self.addressManager
            self.addressManager = None
        self.client = None
        self.socket = None

    def _callback(self, socket, client, data):
        if self.addressManager is not None:
            self.socket = socket
            self.client = client
            self.addressManager.handle(data)

    def add(self, callback, oscAddress):
        """add a callback for oscAddress"""
        if self.addressManager is not None:
            self.addressManager.add(callback, oscAddress)

    def sendMsg(self, oscAddress, dataArray=[]):
        """send an OSC-message to connected client(s)"""
        if self.socket is not None and self.client is not None:
            self.socket.sendto( osc.createBinaryMsg(oscAddress, dataArray),  self.client)

    def sendBundle(self, bundle):
        """send an OSC-bundle to connected client(s)"""
        if self.socket is not None and self.client is not None:
            self.socket.sendto(bundle.message, self.client)

class NetClient:
    """ OSC-client running on GOD.
    sends OSC-messages to SMi.
    receives OSC-messages from SMi (and emits signals with the data),
    """
    def __init__(self, host, port):
        print "NetClient"

def _callback(message, source):
    print "callback (no class): ", message

class _TestServer:
    def __init__(self):
        self.serv = NetServer()
        self.serv.add(self.callback, '/test')

    def __del__(self):
        if self.serv is not None:
            self.serv.shutdown()
            del self.serv
            self.serv = None

    def callback(self, message, source):
        self.serv.sendMsg(message[0], message[2:])

def test_server():
    import time
    n = _TestServer()
    time.sleep(50)
    print "cleanup"
    n.__del__()
    del n
    n = None
    time.sleep(10)


if __name__ == '__main__':
    test_server()
