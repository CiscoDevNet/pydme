"""
PyDME - Python Bindings for DME REST API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PyDME is a simplified take on providing Python bindings for Cisco DME
REST API.

"""

__title__ = 'pydme'
__version__ = '1.0'
__build__ = 1
__author__ = 'Sai Chintalapudi'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright (c) 2020 Cisco Systems, Inc. All rights reserved.'


from .core import Node
import pydme.options
import pydme.filters
