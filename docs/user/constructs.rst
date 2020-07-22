Constructs
==========

PyDME tries to provide a minimal set of constructs, that should be
enough to achieve most of the tasks that would otherwise be achieved
using the REST API.

Node
----

A Node represents the nexus node that one would be communicating
with. This could be a standalone, leaf or spine. A Node object can be
instantiated by specifying the REST URL for communicating with the
underlying node.

    >>> from pydme import Node
    >>> nxsw = Node('https://192.168.10.1')

It is also possible to provide DME meta data file to when the Node
object is instantiated.

    >>> nxsw = Node('https://192.168.10.1', 'path/to/dme-meta.json')

The default way is to not provide the DME meta file so that PyDME will
automatically get the version of the device and gets the proper DME
meta file based on that version and uses it.

For more information, refer to Node documentation.

API Objects
-----------

Once a Node has been instantiated, a variety of API objects can be
spawned from that. There are two classes of these objects:

- Methods
- Managed objects

All these objects support one, or many REST operations. The objects are
local instances and objects don't interact with the underlying physical
node. In order to interact, one of the supported REST construct has to be
invoked on them. There are utmost three REST constructs supported on
these objects:

- GET
- POST
- DELETE

Methods
-------

Any REST request that does not operate on managed objects is modeled
as a method. The following are some of the methods that are currently
supported:

Login
~~~~~

This method supports a simple password based login.

    >>> nxsw.methods.Login('admin', 'password').POST()

LoginRefresh
~~~~~~~~~~~~

This method refreshes an existing session.

    >>> nxsw.methods.LoginRefresh().GET()

Managed Objects
---------------

DME managed objects can be instantiated fromt the Node object using a
local Managed Information Tree (MIT). Each invocation of `mit`
property on the Node object will result in a different local MIT which
can be used as a local cache. For instance, a local topSystem object can
be instantiated as follows:

    >>> mit = nxsw.mit
    >>> mit.topSystem()

Please note that at this point this object is only locally
instantiated.

At this point, you would have noticed that . notation is used to chain
object containment hierarchy. The same . notation is also used for
accessing properties of an object.

    >>> user = nxsw.mit.topSystem().snmpEntity().
    ... snmpInst().snmpLocalUser('test')
    >>> user.ipv4AclName = '4acl'
    >>> print user.ipv4AclName
    4acl
    >>> print user.Xml
    <snmpLocalUser userName="test" ipv4AclName="4acl"/>

When using . notation for a child object, one should specify the class
name, followed by a paranthesis that takes naming properties as either
arguments, or keyword arguments. One can also specify non naming
properties as keyword arguments.

    >>> top = nxsw.mit.topSystem()
    >>> user = top.snmpEntity().snmpInst().snmpLocalUser('test')
    >>> print user.Xml
    <snmpLocalUser userName="test"/>
    
    >>> user = top.snmpEntity().snmpInst().
    ... snmpLocalUser(userName='test')
    >>> print user.Xml
    <snmpLocalUser userName="test"/>
    
    >>> user = top.snmpEntity().snmpInst().
    ... snmpLocalUser('test', ipv4AclName="4acl")
    >>> print user.Xml
    <snmpLocalUser userName="test" ipv4AclName="4acl"/>


POST
~~~~

Local managed objects are posted to underlying node using POST()
method on the object. The following example shows posting of a new
snmpLocaluser to NX-OS device.

    >>> nxsw.mit.topSystem().snmpEntity().snmpInst().
    ... snmpLocalUser('test').POST()

DELETE
~~~~~~

Local managed objects can be deleted from the underlying node using
DELETE() method on that object. An snmpLocalUser object can be deleted
as shown below:

    >>> nxsw.mit.topSystem().snmpEntity().snmpInst().
    ... snmpLocalUser('test').DELETE()

Please note that the local cached managed objects still remain even
though it is deleted from NX-OS device. To update the local objects,
if needed, GET() method can be used as shown below.

GET
~~~

Local managed objects can be fetched from the underlying node using
GET() method on that object. GET() takes other option to affect the
scope of the query. We'll look at them later. To begin with, an
snmpLocalUser can be fetched as follows:

    >>> bd = nxsw.mit.topSystem().snmpEntity().snmpInst().
    ... snmpLocalUser('test')
    >>> result = bd.GET()
    >>> type(result)
    <type 'list'>
    >>> print len(result)
    1
    >>> print result[0].Dn
    sys/snmp/inst/lclUser-test

Please note that the GET() method returs a list. The monadic nature of
list is taken advantage to represent the result of a query that can
fetch 0, 1 or more objects. It should also be noted that the local
managed object is automatically updated with the fetched values.

    >>> print bd.Xml
    <snmpLocalUser dn="sys/snmp/inst/lclUser-test" usrengineIdlen="0" modTs="2019-12-11T22:51:08.735+00:00" childAction="" status="" userName="test" authtype="no" ipv4AclName="4acl" authpwd="" privpwd="" isenforcepriv="no" islocalizedkey="no" ipv6AclName="" privtype="no" usrengineId=""/>

GET() method can be combined with various options to result in more
powerful queries like fetching objects of a certain class, or subtree,
etc. For instance, all users can be queries as follows:

    >>> from pydme import options
    >>> result = nxsw.mit.GET(**options.subtreeClass('snmpLocalUser'))
    >>> for user in result:
    ...     print user.Dn
    ...
    sys/snmp/inst/lclUser-admin
    sys/snmp/inst/lclUser-test

The entire subtree of snmpEntity can be queried as follows:

    >>> result = nxsw.mit.polUni().snmpEntity().GET(**options.subtree)
    >>> for entity in result:
    ...     print entity.Dn
    ...
    sys/snmp/inst/lclUser-admin/group-network-admin
    sys/snmp/inst/lclUser-admin
    sys/snmp/inst/lclUser-test
    sys/snmp/inst/rmon/event-4
    sys/snmp/inst/rmon/event-2
    sys/snmp/inst/rmon/event-5
    sys/snmp/inst/rmon/event-1
    sys/snmp/inst/rmon/event-3
    sys/snmp/inst/rmon
    sys/snmp/inst/traps/aaa/serverstatechange
    sys/snmp/inst/traps/aaa
    sys/snmp/inst/traps/bfd/sessiondown
    sys/snmp/inst/traps/bfd/sessionup
    sys/snmp/inst/traps/bfd
    sys/snmp/inst/traps/bridge/newroot
    sys/snmp/inst/traps/bridge/topologychange
    sys/snmp/inst/traps/bridge
    sys/snmp/inst/traps/callhome/eventnotify
    sys/snmp/inst/traps/callhome/smtpsendfail
    sys/snmp/inst/traps/callhome
    sys/snmp/inst/traps/cfs/mergefailure
    sys/snmp/inst/traps/cfs/statechangenotif
    sys/snmp/inst/traps/cfs
    sys/snmp/inst/traps/config/ccmCLIRunningConfigChanged
    sys/snmp/inst/traps/config
    sys/snmp/inst/traps/entity/entityfanstatuschange
    sys/snmp/inst/traps/entity/entitymibchange
    sys/snmp/inst/traps/entity/cefcMIBEnableStatusNotification
    sys/snmp/inst/traps/entity/entitymoduleinserted
    sys/snmp/inst/traps/entity/entitymoduleremoved
    sys/snmp/inst/traps/entity/entitymodulestatuschange
    sys/snmp/inst/traps/entity/entitypoweroutchange
    sys/snmp/inst/traps/entity/entitypowerstatuschange
    sys/snmp/inst/traps/entity/entitysensor
    sys/snmp/inst/traps/entity/entityunrecognisedmodule
    sys/snmp/inst/traps/entity
    sys/snmp/inst/traps/featurecontrol/ciscoFeatOpStatusChange
    sys/snmp/inst/traps/featurecontrol/FeatureOpStatusChange
    sys/snmp/inst/traps/featurecontrol
    sys/snmp/inst/traps/generic/coldStart
    sys/snmp/inst/traps/generic/warmStart
    sys/snmp/inst/traps/generic
    sys/snmp/inst/traps/hsrp/statechange
    sys/snmp/inst/traps/hsrp
    sys/snmp/inst/traps/ip/sla
    sys/snmp/inst/traps/ip
    sys/snmp/inst/traps/license/notifylicenseexpiry
    sys/snmp/inst/traps/license/notifylicenseexpirywarning
    sys/snmp/inst/traps/license/notifylicensefilemissing
    sys/snmp/inst/traps/license/notifynolicenseforfeature
    sys/snmp/inst/traps/license
    sys/snmp/inst/traps/link/cerrdisableinterfaceeventrev1
    sys/snmp/inst/traps/link/cieLinkDown
    sys/snmp/inst/traps/link/cieLinkUp
    sys/snmp/inst/traps/link/ciscoxcvrmonstatuschg
    sys/snmp/inst/traps/link/cmnmacmovenotification
    sys/snmp/inst/traps/link/delayedlinkstatechange
    sys/snmp/inst/traps/link/extendedlinkDown
    sys/snmp/inst/traps/link/extendedlinkUp
    sys/snmp/inst/traps/link/linkDown
    sys/snmp/inst/traps/link/linkUp
    sys/snmp/inst/traps/link
    sys/snmp/inst/traps/lldp/lldpRemTablesChange
    sys/snmp/inst/traps/lldp
    sys/snmp/inst/traps/mmode/cseMaintModeChangeNotify
    sys/snmp/inst/traps/mmode/cseNormalModeChangeNotify
    sys/snmp/inst/traps/mmode
    sys/snmp/inst/traps/msdp/msdpBackwardTransition
    sys/snmp/inst/traps/msdp
    sys/snmp/inst/traps/pim/pimNeighborLoss
    sys/snmp/inst/traps/pim
    sys/snmp/inst/traps/poe/controlenable
    sys/snmp/inst/traps/poe/policenotify
    sys/snmp/inst/traps/poe
    sys/snmp/inst/traps/portsecurity/accesssecuremacviolation
    sys/snmp/inst/traps/portsecurity/trunksecuremacviolation
    sys/snmp/inst/traps/portsecurity
    sys/snmp/inst/traps/rf/redundancyframework
    sys/snmp/inst/traps/rf
    sys/snmp/inst/traps/rmon/fallingAlarm
    sys/snmp/inst/traps/rmon/hcFallingAlarm
    sys/snmp/inst/traps/rmon/hcRisingAlarm
    sys/snmp/inst/traps/rmon/risingAlarm
    sys/snmp/inst/traps/rmon
    sys/snmp/inst/traps/snmp/authentication
    sys/snmp/inst/traps/snmp
    sys/snmp/inst/traps/stormcontrol/cpscEventRev1
    sys/snmp/inst/traps/stormcontrol
    sys/snmp/inst/traps/stpx/inconsistency
    sys/snmp/inst/traps/stpx/loopinconsistency
    sys/snmp/inst/traps/stpx/rootinconsistency
    sys/snmp/inst/traps/stpx
    sys/snmp/inst/traps/sysmgr/cseFailSwCoreNotifyExtended
    sys/snmp/inst/traps/sysmgr
    sys/snmp/inst/traps/system/Clockchangenotification
    sys/snmp/inst/traps/system
    sys/snmp/inst/traps/upgrade/UpgradeJobStatusNotify
    sys/snmp/inst/traps/upgrade/UpgradeOpNotifyOnCompletion
    sys/snmp/inst/traps/upgrade
    sys/snmp/inst/traps/vsan/vsanPortMembershipChange
    sys/snmp/inst/traps/vsan/vsanStatusChange
    sys/snmp/inst/traps/vsan
    sys/snmp/inst/traps/vtp/notifs
    sys/snmp/inst/traps/vtp/vlancreate
    sys/snmp/inst/traps/vtp/vlandelete
    sys/snmp/inst/traps/vtp
    sys/snmp/inst/traps
    sys/snmp/inst
    sys/snmp/servershutdown
    sys/snmp

Multiple options can be combined with & operator, and filters can be used as follows:

    >>> for user in nxsw.mit.topSystem().GET(
    ...     **options.subtreeClass('snmpLocalUser') &
    ...     options.filter(filters.Eq('snmpLocalUser.userName', 'test'))):
    ...     print user.Dn
    ...
    sys/snmp/inst/lclUser-test

Managed Object Iterators
------------------------

Local MIT provides a construct of object iterators. On a given
object, . notation can be used with (immediate) child class name
without a following paranthesis to access all children of that
class. For instance:

    >>> mit = nxsw.mit
    >>> mit.topSystem().snmpEntity().snmpInst().snmpLocalUser('test1')
    >>> mit.topSystem().snmpEntity().snmpInst().snmpLocalUser('test2')
    >>> mit.topSystem().snmpEntity().snmpInst().snmpLocalUser('test3')
    >>> for user in mit.topSystem().snmpEntity().snmpInst().snmpLocalUser:
    ...     print user.Dn
    ...
    sys/snmp/inst/lclUser-test1
    sys/snmp/inst/lclUser-test2
    sys/snmp/inst/lclUser-test3

The use of iterators becomes more obvious when one is walking through
a subtree that is fetched from a node.

    >>> inst = nxsw.mit.topSystem().snmpEntity().snmpInst()
    >>> inst.GET(**options.subtree)
    >>> for user in inst.snmpLocalUser:
    ...     print user.userName, user.Dn, user.modTs
    ...
    admin sys/snmp/inst/lclUser-admin 2019-12-11T20:21:27.694+00:00
    test sys/snmp/inst/lclUser-test 2019-12-11T23:52:18.686+00:00

There is also a way to access all the children of a given object using
Children property.

    >>> inst = nxsw.mit.topSystem().snmpEntity().snmpInst()
    >>> inst.GET(**options.subtree)
    >>> for child in inst.Children:
    ...     print child.Dn
    ...
    sys/snmp/inst/lclUser-admin
    sys/snmp/inst/lclUser-test
    sys/snmp/inst/rmon
    sys/snmp/inst/traps

Event Subscription
------------------------

Listening to events of a particular MO and all its children can
be derived from DME managed objects of the node.
For instance, to listen to all the physical interface events,
when changing mtu and description of an interface:

    >>> nxsw.startWsListener()
    >>> _, subscriptionId = nxsw.methods.ResolveClass('l1PhysIf').
    ... GET(**options.subscribe & options.subtree)
    >>> nxsw.waitForWsMo(subscriptionId)
    >>> if nxsw.hasWsMo(subscriptionId):
    ...     print nxsw.popWsMo(subscriptionId).Xml
    ...
    <ethpmPhysIf dn="sys/intf/phys-[eth1/1]/phys"
    ... rn="" status="modified" childAction="" operDescr="goodInterface"/>
    <ethpmPhysIf dn="sys/intf/phys-[eth1/1]/phys" rn=""
    ... status="modified" operMtu="1500" childAction="" userCfgdFlags=""/>

Example code
-------------

Complete code examples are provided `here <https://github.com/CiscoDevNet/pydme/blob/master/examples/>`_

These examples assume that user knows the path from topSystem to the managed object. In case, it is not
known, `buildMoTree <https://github.com/CiscoDevNet/pydme/blob/master/utils/buildMoTree.py>`_ can be used
which can determine the parents of the given managed object which include the name paremeters as well. This
utility can also provide the properties of the managed object and its children.

- example: python buildMoTree.py ./dme-9.3.5-meta.json rtctrlRttP (where rtctrlRttP is the managed object)

.. image:: ./mo_p.png
   :height: 300
   :width: 600

Supported Version
-----------------

PyDME is supported on N9K running version 9.3(5) or above. 
The DME model documentation is `here <https://developer.cisco.com/site/nxapi-dme-model-reference-api/>`_
