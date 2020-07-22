import logging
import os
#pylint: disable=unused-import
import sure                     # flake8: noqa
import sys

paths = [
    '..',
]
for path in paths:
    sys.path.append(os.path.abspath(path))

import pydme

logging.captureWarnings(True)

def testSubtreeClass():
    opt = pydme.options.subtreeClass('fvSubnet')
    opt['query-target'].should.equal('subtree')
    opt['target-subtree-class'].should.equal('fvSubnet')

def testChildClass():
    opt = pydme.options.childClass('fvSubnet')
    opt['query-target'].should.equal('children')
    opt['target-subtree-class'].should.equal('fvSubnet')

def testOrderBy():
    opt = pydme.options.orderBy('fvSubnet.addr')
    opt['order-by'].should.equal('fvSubnet.addr')

def testPage():
    opt = pydme.options.page(1) & pydme.options.pageSize(50)
    opt['page'].should.equal(1)
    opt['page-size'].should.equal(50)

def testFilter():
    opt = pydme.options.filter(pydme.filters.Eq('fvTenant.name', 'cisco'))
    opt['query-target-filter'].should.equal('eq(fvTenant.name,"cisco")')
