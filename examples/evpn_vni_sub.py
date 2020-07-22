from __future__ import print_function
#!/usr/bin/env python

import sys
import os
import json
import logging

from pydme import Node, options, filters

# This example shows how to subscribe and listen to
# events of evpn vni configuration.

def main(host, user, password, **kwargs):
    print('Initializing connection to nexus device ...')
    nxswUrl = 'http://%s' % (host)
    nxsw = Node(nxswUrl)
    nxsw.methods.Login(user, password, autoRefresh=True).POST()
    print('Listening for Events ...')
    nxsw.startWsListener()
    _, subscriptionId = nxsw.methods.ResolveClass('rtctrlL2Evpn').GET(**options.subscribe & options.subtree)
    while(True):
        nxsw.waitForWsMo(subscriptionId, timeout=5)
        if nxsw.hasWsMo(subscriptionId):
            print(nxsw.popWsMo(subscriptionId).Xml)
    print('logging out')
    nxsw.methods.Logout(user)

if __name__ == '__main__':
    # Fill in host, user, pw here
    main(host, username, password)
    print('success')
