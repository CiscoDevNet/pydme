#!/usr/bin/env python

import sys
import os
import json
import logging
import random
import socket
import struct
from ipaddress import IPv4Address

from pydme import Node, options, filters

# This example code creates evpn vni configuration with
# vni ranging from 6000 to 6009. The rest of the configuration
# is auto generated using random numbers.

def isValidIp(ip):
    try:
        IPv4Address(ip)
        return True
    except ValueError:
        return False

def getAsNn(target):
    if target == 'auto':
        return 'unknown:0:0'
    lt = target.split(':')
    if isValidIp(lt[0]):
        return 'ipv4-nn2:' + target
    if int(lt[0]) > 65535:
        return 'as4-nn2:' + target
    else:
        if int(lt[1]) > 65535:
            return 'as2-nn4:' + target
        else:
            return 'as2-nn2:' + target

def loginNode(host, user, password):
    print('Initializing connection to nexus device ...')
    nxswUrl = 'https://%s' % (host)
    nxsw = Node(nxswUrl)
    nxsw.methods.Login(user, password).POST()
    mit = nxsw.mit
    return nxsw, mit

def setup(mit):
    feature_bgp = mit.topSystem().fmEntity().fmBgp()
    feature_bgp.adminSt = 'enabled'
    resp = feature_bgp.POST()
    feature_nv_overlay_evpn = mit.topSystem().fmEntity().fmEvpn()
    feature_nv_overlay_evpn.adminSt = 'enabled'
    feature_nv_overlay_evpn.POST()
    evpn = mit.topSystem().rtctrlL2Evpn()
    evpn.adminSt = 'enabled'
    return evpn

def postConfig(evpn):
    evpn.POST()

def setConfig(evpn, **kwargs):
    vni = evpn.rtctrlBDEvi('vxlan-' + kwargs['vni'])
    vni.rd = 'rd:' + getAsNn(kwargs['rd'])
    rti = vni.rtctrlRttP('import')
    for item in kwargs['rti']:
        rti.rtctrlRttEntry('route-target:' + getAsNn(item))
    rte = vni.rtctrlRttP('export')
    for item in kwargs['rte']:
        rte.rtctrlRttEntry('route-target:' + getAsNn(item))
    return evpn

def logoutNode(switch, user):
    print('logging out')
    switch.methods.Logout(user)

if __name__ == '__main__':
    rti = ['auto']
    rte = ['auto']
    # Fill in host, user, pw here
    nxsw, mit = loginNode(host, username, password)
    evpn = setup(mit)
    for i in range(0, 10):
        vni = str((6000 + i))
        rd = str(random.randint(1,100)) + ':' + str(random.randint(1,10))
        rti.append(str(random.randint(1,10000)) + ':' + str(random.randint(1,100)))
        rti.append(str(socket.inet_ntoa(struct.pack("!I", random.randint(1000000000,2000000000)))+':'+str(random.randint(1,100))))
        rte.append(str(random.randint(1,10000)) + ':' + str(random.randint(1,100)))
        rte.append(str(random.randint(1,10000)) + ':' + str(random.randint(1,100)))
        setConfig(evpn, vni=vni, rd=rd, rti=rti, rte=rte)
        rti = ['auto']
        rte = ['auto']
    postConfig(evpn)
    # Fill in user here
    logoutNode(nxsw, username)
    print('success')
