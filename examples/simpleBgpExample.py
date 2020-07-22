from __future__ import print_function
#!/usr/bin/env python

import json

from pydme import Node

# Fill in host, username, password here
username = ''
password = ''
host = ''

# This method is used to login to the NX-OS node
def loginNode():
    print('=> Initializing connection to nexus device ...')
    nxswUrl = 'https://%s' % (host)
    nxsw = Node(nxswUrl)
    nxsw.methods.Login(username, password).POST()
    mit = nxsw.mit
    return nxsw, mit

# This method is used to enable bgp feature
def enableBgpFeature(feature_bgp):
    print('=> Enabling bgp feature')
    feature_bgp.adminSt = 'enabled'
    feature_bgp.POST()

# This method is used to create bgp router with asn as 1
def createBgpRouter(bgpEntity, asn):
    print('=> creating bgp router with asn 1')
    bgpEntity.adminSt = 'enabled'
    bgpInst = bgpEntity.bgpInst()
    bgpInst.asn = asn
    bgpEntity.POST()

# This method is used to get and print the bgp configuration
def getConfig(bgp):
    print("\n--------------------------------------------------")
    print('=> getting bgp configuration')
    result = bgp.GET()
    if result:
        print(bgp.Json)
    else:
        print('no bgp config')
    print("--------------------------------------------------")
    
# This method is used to delete the bgp router
def deleteConfig(bgpEntity, feature_bgp):
    print('=> deleting bgp router')
    # remove bgp instance
    bgpInst = bgpEntity.bgpInst()
    bgpInst.DELETE()
    # remove bgp entity
    bgpEntity.DELETE()
    print('=> removing bgp feature')
    feature_bgp.adminSt = 'disabled'
    feature_bgp.POST()

# This method is used to logout of the NX-OS node
def logoutNode(switch, user):
    print('=> logging out of node')
    switch.methods.Logout(user)

if __name__ == '__main__':
    nxsw, mit = loginNode()
    feature_bgp = mit.topSystem().fmEntity().fmBgp()
    bgpEntity = mit.topSystem().bgpEntity()
    bgpInst = bgpEntity.bgpInst()
    getConfig(bgpInst)
    enableBgpFeature(feature_bgp)
    createBgpRouter(bgpEntity, '1')
    getConfig(bgpInst)
    deleteConfig(bgpEntity, feature_bgp)
    getConfig(bgpInst)
    logoutNode(nxsw, username)
    print('success')
