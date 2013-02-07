#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

TYPE = '_mintOSC._udp'

if_index2name=[]
try:
    import netifacesP
    if_index2name = netifaces.interfaces()
except: pass

def if_indextoname(index):
    try:
        ifname=if_index2name[index-1]
    except:
        ifname="net:%02d" % (index)
    return ifname

class ZeroConf:

##    def service_resolved(self, *args):
##        print "resolved: ", args
##        print "name: ", args[2]
##        print "address: %s:%d" % (args[7],args[8])
##        print "iface: ", args
##
##    def print_error(self, *args):
##        print 'error_handler', args

    def newHandler(self, arg_interface, arg_protocol, arg_name, arg_stype, arg_domain, arg_flags):
        interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags = self.server.ResolveService(
            arg_interface, arg_protocol, arg_name, arg_stype, arg_domain,
            avahi.PROTO_UNSPEC, dbus.UInt32(0))

        print "name: ", name
        print "address: %s:%d" % (address, port)
        print "iface: ", if_indextoname(interface)
        print ""

##        ifname=if_indextoname(interface)
##        # the following handlers get called asynchronously
##        self.server.ResolveService(interface, protocol, name, stype, domain,
##                                   avahi.PROTO_UNSPEC, dbus.UInt32(0), 
##                                   reply_handler=self.service_resolved,
##                                   error_handler=self.print_error)

    def __init__(self, domain='local'):
        loop = DBusGMainLoop()
        bus = dbus.SystemBus(mainloop=loop)
        self.server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
                                      avahi.DBUS_INTERFACE_SERVER)
        sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
                                                 self.server.ServiceBrowserNew(avahi.IF_UNSPEC,
                                                                               avahi.PROTO_INET,
                                                                               TYPE,
                                                                               domain,
                                                                               dbus.UInt32(0))),
                                  avahi.DBUS_INTERFACE_SERVICE_BROWSER)
        sbrowser.connect_to_signal("ItemNew", self.newHandler)


if __name__ == '__main__':
    zc = ZeroConf()
    gobject.MainLoop().run()
