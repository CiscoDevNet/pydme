import httpretty

from lxml import etree
import logging
import os
#pylint: disable=unused-import
import sure                     # flake8: noqa
import sys
import textwrap
import unittest
import time

paths = [
    '..',
]
for path in paths:
    sys.path.append(os.path.abspath(path))

import pydme

logging.captureWarnings(True)

url = 'https://localhost'


class MoTests(unittest.TestCase):
    def setUp(self):
        self.api = pydme.Node(url)
        self.api.methods.Login(
            'jsmith', 'secret').POST()
        self.tree = self.api.mit

    def testPolUni(self):
        uni = self.tree.polUni()
        uni.Rn.should.equal('uni')
        uni.Dn.should.equal('uni')
        uni._url().should_not.be.different_of(
            url + '/api/mo/' + uni.Dn + '.xml'
        )

    def testFvTenant(self):
        tenant = self.tree.polUni().fvTenant('common')
        tenant.Rn.should.equal('tn-[common]')
        tenant.Dn.should.equal('uni/tn-[common]')
        tenant._url().should_not.be.different_of(
            url + '/api/mo/' + tenant.Dn + '.xml'
        )

    def testFvTenantOptionalArgs(self):
        tenant = self.tree.polUni().fvTenant('common', descr='Common tenant')
        tenant.Dn.should.equal('uni/tn-[common]')
        tenant.descr.should.equal('Common tenant')

    def testFvTenantFromKeywordArguments(self):
        tenant = self.tree.polUni().fvTenant(
            name='common', descr='Common tenant'
        )
        tenant.Dn.should.equal('uni/tn-[common]')
        tenant.descr.should.equal('Common tenant')

    def testUrl(self):
        mos = self.api.mit
        mos._url().should.equal(url + '/api/mo.xml')

    def testUniFromDn(self):
        uni = self.api.mit.FromDn('uni')
        uni.should.be.an(pydme.core.Mo)
        uni.ClassName.should.equal('polUni')
        uni.Dn.should.equal('uni')

    def testTenantFromDn(self):
        tenant = self.api.mit.FromDn('uni/tn-[common]')
        tenant.should.be.an(pydme.core.Mo)
        tenant.ClassName.should.equal('fvTenant')
        tenant.name.should.equal('common')
        tenant.Dn.should.equal('uni/tn-[common]')

    def testEpPFromDn(self):
        epp = self.api.mit.FromDn(
            'uni/epp/fv-[uni/tn-infra/ap-access/epg-default]'
        )
        epp.should.be.an(pydme.core.Mo)
        epp.ClassName.should.equal('fvEpP')
        epp.epgPKey.should.equal('uni/tn-infra/ap-access/epg-default')
        epp.Dn.should.equal('uni/epp/fv-[uni/tn-infra/ap-access/epg-default]')

    def testJson(self):
        uni = self.tree.polUni()
        tenant = uni.fvTenant('mgmt')
        tenant.Json.should_not.be.different_of(textwrap.dedent('''\
        {
          "fvTenant": {
            "attributes": {
              "name": "mgmt"
            }
          }
        }'''))

        uni.Json.should_not.be.different_of(textwrap.dedent('''\
        {
          "polUni": {
            "children": [
              {
                "fvTenant": {
                  "attributes": {
                    "name": "mgmt"
                  }
                }
              }
            ]
          }
        }'''))

    def testJsonSetter(self):
        tenant = self.tree.polUni().fvTenant('common')
        tenant.Json = textwrap.dedent('''\
        {
          "fvTenant": {
            "attributes": {
              "name": "common",
              "descr": "Common tenant for sharing"
            }
          }
        }''')
        tenant.name.should.equal('common')
        tenant.descr.should.equal('Common tenant for sharing')

    def testJsonSetterTree(self):
        tree = textwrap.dedent('''\
        {
          "polUni": {
            "children": [
              {
                "fvTenant": {
                  "attributes": {
                    "name": "test"
                  },
                  "children": [
                    {
                      "fvBD": {
                        "attributes": {
                          "name": "lab"
                        },
                        "children": [
                          {
                            "fvRsCtx": {
                              "attributes": {
                                "tnFvCtxName": "infra"
                              }
                            }
                          }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          }
        }''')
        uni = self.tree.polUni()
        uni.Json = tree
        uni.Json.should_not.be.different_of(tree)

    def testXml(self):
        uni = self.tree.polUni()
        tenant = uni.fvTenant('mgmt')
        tenant.Xml.should_not.be.different_of('<fvTenant name="mgmt"/>\n')

        uni.Xml.should_not.be.different_of(textwrap.dedent('''\
        <polUni>
          <fvTenant name="mgmt"/>
        </polUni>
        '''))

    def testXmlSetter(self):
        tenant = self.tree.polUni().fvTenant('common')
        tenant.Xml = '<fvTenant name="common" descr="Common tenant"/>'
        tenant.name.should.equal('common')
        tenant.descr.should.equal('Common tenant')

    def testXmlSetterTree(self):
        uni = self.tree.polUni()
        tree = textwrap.dedent('''\
        <polUni>
          <fvTenant name="test">
            <fvBD name="lab">
              <fvRsCtx tnFvCtxName="infra"/>
            </fvBD>
          </fvTenant>
        </polUni>
        ''')
        uni.Xml = tree
        uni.Xml.should_not.be.different_of(tree)

    def testMoWithNoNamingProperties(self):
        uni = self.tree.polUni()
        uni.fvTenant('test').fvBD('lab').fvRsCtx().tnFvCtxName = 'infra'
        uni.Xml.should_not.be.different_of(textwrap.dedent('''\
        <polUni>
          <fvTenant name="test">
            <fvBD name="lab">
              <fvRsCtx tnFvCtxName="infra"/>
            </fvBD>
          </fvTenant>
        </polUni>
        '''))

    def testPropertySetter(self):
        tenant = self.tree.polUni().fvTenant('mgmt')
        tenant.descr.should.be(None)
        tenant.descr = 'Sample description'
        tenant.descr.should.equal('Sample description')
        et = etree.XML(tenant.Xml)
        et.tag.should.equal('fvTenant')
        et.attrib['name'].should.equal('mgmt')
        et.attrib['descr'].should.equal('Sample description')

    def testMoChaining(self):
        uni = self.tree.polUni()
        (uni.fvTenant('test').
         fvCtx('infra').Up().
         fvBD('lab').fvRsCtx(tnFvCtxName='infra').Up(2).
         fvBD('hr').fvRsCtx(tnFvCtxName='infra'))
        uni.Xml.should_not.be.different_of(textwrap.dedent('''\
        <polUni>
          <fvTenant name="test">
            <fvCtx name="infra"/>
            <fvBD name="lab">
              <fvRsCtx tnFvCtxName="infra"/>
            </fvBD>
            <fvBD name="hr">
              <fvRsCtx tnFvCtxName="infra"/>
            </fvBD>
          </fvTenant>
        </polUni>
        '''))

    def testNotEnoughNamingProperties(self):
        uni = self.tree.polUni()
        uni.fvBDDef.when.called_with('dontcare').should.throw(
            pydme.errors.MoError,
            'Class `fvBDDef` requires 2 naming properties, '
            'but only 1 were provided')

    def testNoNamingProperties(self):
        uni = self.tree.polUni()
        uni.fvBDDef.when.called_with().should.throw(
            pydme.errors.MoError,
            'Missing naming property `bdDn` for class `fvBDDef`')

    def testUpTooMany(self):
        uni = self.tree.polUni()
        uni.Up.when.called_with(2).should.throw(
            pydme.errors.MoError,
            'Reached topRoot after 1 levels'
        )

    def testParseXmlWithoutDn(self):
        xml=textwrap.dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <imdata totalCount="1">
            <fvTenant name="mgmt"/>
        </imdata>''')
        (self.tree.ParseXmlResponse
         .when.called_with(xml).should.throw(
             pydme.errors.MoError,
             'Property `dn` not found in element <fvTenant name="mgmt"/>'
         ))

    def testParseJsonWithoutDn(self):
        text=textwrap.dedent('''\
        {
          "imdata":[
            {
              "fvTenant":{
                "attributes":{
                  "name":"mgmt"
                }
              }
            }
          ],
          "totalCount":"1"
        }
        ''')
        (self.tree.ParseJsonResponse
         .when.called_with(text).should.throw(
             pydme.errors.MoError,
             "Property `dn` not found in dict"
         ))

    def testWrongXmlElement(self):
        et = etree.XML('<fvTenant name="test"/>')
        self.tree.polUni()._fromXmlElement.when.called_with(et).should.throw(
            pydme.errors.MoError,
            'Root element tag `fvTenant` does not match with class `polUni`'
        )


class LoginTests(unittest.TestCase):
    def setUp(self):
        self.login = pydme.Node(url).methods.Login(
            'jsmith', 'secret'
        )

    def testCreation(self):
        self.login._url().should.equal(url + '/api/aaaLogin.xml')
        et = etree.XML(self.login.Xml)
        et.tag.should.equal('aaaUser')
        et.attrib['name'].should.equal('jsmith')
        et.attrib['pwd'].should.equal('secret')
        self.login.Json.should.equal(textwrap.dedent('''\
        {
          "aaaUser": {
            "attributes": {
              "name": "jsmith",
              "pwd": "secret"
            }
          }
        }'''))

    @httpretty.activate
    def testJsonPOST(self):
        httpretty.register_uri(httpretty.POST,
                               url + '/api/aaaLogin.json')
        self.login.POST(format='json')
        (httpretty.last_request().method).should.equal('POST')
        (httpretty.last_request().path).should.equal('/api/aaaLogin.json')
        (httpretty.last_request().body.decode("utf-8")).should.equal(self.login.Json)

    @httpretty.activate
    def testXmlPOST(self):
        xml_body = '''<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1">
<aaaLogin token="f00AAAAAAAAAAAAAAAAAAK4wjyQODSwoW3hizW066Ts6Gs2S4fkFZf6XhK32II8gZrRrgVGF2Y0pPs05FntrA6LCwXFWicPGpgsUp+SqTJdHZMeQrn45HBxJrmSJKtuYiqCX5Qc5P67Qq+c4w+VDcsHZxXe7KqeUs1TfKlXvvco8CwPOCRWJzMly0ArRsEL6c4t5zQTYpy9XsGwQEWJD/A==" siteFingerprint="UAViQctMne4xvtyZ" refreshTimeoutSeconds="600" maximumLifetimeSeconds="86400" guiIdleTimeoutSeconds="1200" restTimeoutSeconds="90" creationTime="1545696032" firstLoginTime="1545696032" userName="admin" remoteUser="false" unixUserId="15374" sessionId="LlQAR9nARFiVBAJWpwrTBQ==" lastName="" firstName="" changePassword="no" version="4.1(0.90b)" buildTime="Fri Oct 26 16:18:38 PDT 2018" node="topology/pod-1/node-1">
<aaaUserDomain name="all" rolesR="admin" rolesW="admin">
<aaaReadRoles/>
<aaaWriteRoles>
<role name="admin"/>
</aaaWriteRoles>
</aaaUserDomain>
<DnDomainMapEntry dn="uni/tn-mgmt" readPrivileges="admin" writePrivileges="admin"/>
<DnDomainMapEntry dn="uni/tn-infra" readPrivileges="admin" writePrivileges="admin"/>
<DnDomainMapEntry dn="uni/tn-common" readPrivileges="admin" writePrivileges="admin"/>
</aaaLogin></imdata>'''
        httpretty.register_uri(httpretty.POST,
                               url + '/api/aaaLogin.xml',
                               body=xml_body,
                               content_type='application/xml',
                               status=200)

        self.login.POST(format='xml')
        (httpretty.last_request().method).should.equal('POST')
        (httpretty.last_request().path).should.equal('/api/aaaLogin.xml')
        (httpretty.last_request().body.decode('utf-8')).should.equal(self.login.Xml)


class LogoutTests(unittest.TestCase):
    def setUp(self):
        self.node = pydme.Node(url)
        self.login = self.node.methods.Login(
            'jsmith', 'secret'
        )
        self.logout = self.node.methods.Logout('jsmith')

    def testCreation(self):
        self.logout._url().should.equal(url + '/api/aaaLogout.xml')
        et = etree.XML(self.logout.Xml)
        et.tag.should.equal('aaaUser')
        et.attrib['name'].should.equal('jsmith')
        self.logout.Json.should.equal(textwrap.dedent('''\
        {
          "aaaUser": {
            "attributes": {
              "name": "jsmith"
            }
          }
        }'''))

    @httpretty.activate
    def testJsonPOST(self):
        httpretty.register_uri(httpretty.POST,
                               url + '/api/aaaLogout.json')
        self.logout.POST(format='json')
        (httpretty.last_request().method).should.equal('POST')
        (httpretty.last_request().path).should.equal('/api/aaaLogout.json')
        (httpretty.last_request().body.decode("utf-8")).should.equal(self.logout.Json)

    @httpretty.activate
    def testXmlPOST(self):
        httpretty.register_uri(httpretty.POST,
                               url + '/api/aaaLogout.xml')

        self.logout.POST(format='xml')
        (httpretty.last_request().method).should.equal('POST')
        (httpretty.last_request().path).should.equal('/api/aaaLogout.xml')
        (httpretty.last_request().body.decode('utf-8')).should.equal(self.logout.Xml)


class LoginRefreshTests(unittest.TestCase):
    def setUp(self):
        self.login = pydme.Node(url).methods.LoginRefresh()

    def testCreation(self):
        self.login._url().should.equal(url + '/api/aaaRefresh.xml')

    @httpretty.activate
    def testAaaUserJsonGET(self):
        httpretty.register_uri(httpretty.GET,
                               url + '/api/aaaRefresh.json')
        self.login.GET(format='json')
        (httpretty.last_request().method).should.equal('GET')
        (httpretty.last_request().path).should.equal('/api/aaaRefresh.json')


class AutoRefreshTests(unittest.TestCase):
    def setUp(self):
        self.node = pydme.Node(url)
        self.login = self.node.methods.Login('jsmith', 'secret', autoRefresh=True)

    @httpretty.activate
    def testRefreshOnce(self):
        login_xml_body = '''<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1">
<aaaLogin token="f00AAAAAAAAAAAAAAAAAAK4wjyQODSwoW3hizW066Ts6Gs2S4fkFZf6XhK32II8gZrRrgVGF2Y0pPs05FntrA6LCwXFWicPGpgsUp+SqTJdHZMeQrn45HBxJrmSJKtuYiqCX5Qc5P67Qq+c4w+VDcsHZxXe7KqeUs1TfKlXvvco8CwPOCRWJzMly0ArRsEL6c4t5zQTYpy9XsGwQEWJD/A==" siteFingerprint="UAViQctMne4xvtyZ" refreshTimeoutSeconds="600" maximumLifetimeSeconds="86400" guiIdleTimeoutSeconds="1200" restTimeoutSeconds="90" creationTime="1545696032" firstLoginTime="1545696032" userName="admin" remoteUser="false" unixUserId="15374" sessionId="LlQAR9nARFiVBAJWpwrTBQ==" lastName="" firstName="" changePassword="no" version="4.1(0.90b)" buildTime="Fri Oct 26 16:18:38 PDT 2018" node="topology/pod-1/node-1">
<aaaUserDomain name="all" rolesR="admin" rolesW="admin">
<aaaReadRoles/>
<aaaWriteRoles>
<role name="admin"/>
</aaaWriteRoles>
</aaaUserDomain>
<DnDomainMapEntry dn="uni/tn-mgmt" readPrivileges="admin" writePrivileges="admin"/>
<DnDomainMapEntry dn="uni/tn-infra" readPrivileges="admin" writePrivileges="admin"/>
<DnDomainMapEntry dn="uni/tn-common" readPrivileges="admin" writePrivileges="admin"/>
</aaaLogin></imdata>'''
        httpretty.register_uri(httpretty.POST,
                               url + '/api/aaaLogin.xml',
                               body=login_xml_body,
                               content_type='application/xml',
                               status=200)

        self.login.POST(format='xml')
        refresh_xml_body = '''<?xml version="1.0" encoding="UTF-8"?><imdata totalCount="1">
<aaaLogin token="700AAAAAAAAAAAAAAAAAAEdiM3Vap8h/9pkqbxgvrOKvPvYW8nkyXIAILMWqdcXSADxXZPE06nsifq+kslkI2UECxR+977d9+yaLtBhK0sz9ugT+id+GFVjh6irHCfIcQDAFeOEYo7u8hxqD84f6iIvGnDzQdZpD4256UkJAZHActeNQzVeDiVS5ldaSEqzAh1Df5IITKKASySUCHi71wg==" siteFingerprint="UAViQctMne4xvtyZ" refreshTimeoutSeconds="600" maximumLifetimeSeconds="86400" guiIdleTimeoutSeconds="1200" restTimeoutSeconds="90" creationTime="1545699898" firstLoginTime="1545699898" userName="admin" remoteUser="false" unixUserId="15374" sessionId="joR4ziDdTeedI1lybx1bjQ==" lastName="" firstName="" changePassword="no" version="4.1(0.90b)" buildTime="Fri Oct 26 16:18:38 PDT 2018" node="topology/pod-1/node-1">
<aaaUserDomain name="all" readRoleBitmask="0" writeRoleBitmask="1"/>
</aaaLogin></imdata>'''
        httpretty.register_uri(httpretty.GET,
                               url + '/api/aaaRefresh.xml',
                               body=refresh_xml_body,
                               content_type='application/xml',
                               status=200
                               )
        self.node._login['nextRefreshBefore']=int(time.time()) - 120
        self.node._autoRefreshThread._refreshLoginIfNeeded()
        (httpretty.last_request().method).should.equal('GET')
        (httpretty.last_request().path).should.equal('/api/aaaRefresh.xml')

        httpretty.register_uri(httpretty.GET,
                               url + '/api/subscriptionRefresh.xml?id=123456789',
                               body='',
                               status=200)
        self.node._wsEvents={}
        self.node._wsEvents['123456789']=[]
        self.node._wsLastRefresh = int(time.time()) - 60
        self.node._autoRefreshThread._refreshSubscriptionsIfNeeded()
        (httpretty.last_request().method).should.equal('GET')
        (httpretty.last_request().path).should.equal('/api/subscriptionRefresh.xml?id=123456789')


class RefreshSubscriptionTests(unittest.TestCase):
    def setUp(self):
        self.node = pydme.Node(url)
        self.rfs = self.node.methods.RefreshSubscriptions('100001')

    def testCreation(self):
        self.rfs._url().should.equal(url + '/api/subscriptionRefresh.xml')

    @httpretty.activate
    def testJsonGET(self):
        httpretty.register_uri(httpretty.GET,
                               url + '/api/subscriptionRefresh.json?id=100001')
        self.rfs.GET(format='json')
        (httpretty.last_request().method).should.equal('GET')
        (httpretty.last_request().path).should.equal('/api/subscriptionRefresh.json?id=100001')

    @httpretty.activate
    def testXmlGET(self):
        httpretty.register_uri(httpretty.GET,
                               url + '/api/subscriptionRefresh.xml?id=100001')

        self.rfs.GET(format='xml')
        (httpretty.last_request().method).should.equal('GET')
        (httpretty.last_request().path).should.equal('/api/subscriptionRefresh.xml?id=100001')


class ResolveClassTests(unittest.TestCase):
    def setUp(self):
        self.api = pydme.Node(url)
        self.api.methods.Login(
            'jsmith', 'secret').POST()
        self.tree = self.api.mit
        self.resolve = self.api.methods.ResolveClass('snmpEntity')

    def testCreation(self):
        self.resolve._url().should.equal(url + '/api/class/snmpEntity.xml')

    @httpretty.activate
    def testJsonGET(self):
        httpretty.register_uri(httpretty.GET,
                               url + '/api/class/snmpEntity.json',
                               body=textwrap.dedent('''\
        {
          "imdata":[
            {
              "snmpEntity": {
                "attributes": {
                "adminSt": "enabled",
                "childAction": "",
                "dn": "sys/snmp",
                "modTs": "2019-12-24T18:53:52.578+00:00",
                "name": "",
                "operErr": "",
                "operSt": "enabled",
                "status": ""
                }
              }
            }
          ],
          "totalCount":"1"
        }
                               '''))
        result = self.resolve.GET(format='json')
        result.shouldnt.be.empty
        tenant = result[0]
        tenant.adminSt.should.equal('enabled')


class MethodsTests(unittest.TestCase):
    def setUp(self):
        self.api = pydme.Node(url)
        self.api.methods.Login(
            'jsmith', 'secret').POST()
        self.tree = self.api.mit

    @httpretty.activate
    def testMoJsonGET(self):
        httpretty.register_uri(httpretty.GET,
                               url + '/api/sys/snmpEntity.json',
                               body=textwrap.dedent('''\
        {
          "imdata":[
            {
              "snmpEntity": {
                "attributes": {
                "adminSt": "enabled",
                "childAction": "",
                "dn": "sys/snmp",
                "modTs": "2019-12-24T18:53:52.578+00:00",
                "name": "",
                "operErr": "",
                "operSt": "enabled",
                "status": ""
                }
              }
            }
          ],
          "totalCount":"1"
        }
                               '''))
        result = self.tree.topSystem().snmpEntity().GET(format='json')
        result = result[0]
        result.should.be.a(pydme.core.Mo)
        result.ClassName.should.equal('snmpEntity')
        result.operSt.should.equal('enabled')

    @httpretty.activate
    def testMoXmlGET(self):
        httpretty.register_uri(httpretty.GET,
                               url + '/api/mo/sys/snmpEntity.xml',
                               body=textwrap.dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <imdata totalCount="1">
            <snmpEntity dn="sys/snmp" status="" name="" childAction=""
                        operErr="" adminSt="enabled"
                        modTs="2019-12-24T18:53:52.578+00:00"
                        operSt="enabled"/>
        </imdata>
                               '''))
        result = self.tree.topSystem().snmpEntity().GET(format='xml')
        result = result[0]
        result.should.be.a(pydme.core.Mo)
        result.ClassName.should.equal('snmpEntity')
        result.operSt.should.equal('enabled')

    @httpretty.activate
    def testMoXmlGETWithOptions(self):
        httpretty.register_uri(
            httpretty.GET,
            url + '/api/mo/sys/snmpEntity.xml?rsp-subtree=full',
            body=textwrap.dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <imdata totalCount="1">
            <snmpEntity dn="sys/snmp" status="" name="" childAction=""
                        operErr="" adminSt="enabled"
                        modTs="2019-12-24T18:53:52.578+00:00"
                        operSt="enabled"/>
        </imdata>
                               '''))
        options = {'rsp-subtree': 'full'}
        result = self.tree.topSystem().snmpEntity().GET(
            format='xml', **options
        )
        result = result[0]
        result.should.be.a(pydme.core.Mo)
        result.ClassName.should.equal('snmpEntity')
        result.operSt.should.equal('enabled')
