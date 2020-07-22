Installation
============

Package Installation
--------------------

You can install from a local or remote archive using ``pip``::

  pip install https://github.com/CiscoDevNet/pydme/blob/master/archive/pydme.zip?raw=true

You can also install from a local directory using ``pip``::

  pip install -e .


DME Meta Data
---------------

PyDME requires metadata about DME model. PyDME gets the software
version of the device during the initialization.

Once it gets the version of the device, it looks for the 
dme-<version>-meta.json file in the current directory for getting
the entire meta data and if it is not found, it will go the web site
and gets it and stores it in the current directory.

If PyDME is unable to get either of these files, it will exit
the program saying the version is not supported.

Note: If the PyDME is cloned from the github and application code
is written using that, then PYDME_HOME environmental variable can be
optionally set to the path of PyDME clone directory. If this is set,
and PyDME cannot find the meta data file in the current directory,
it will look for meta data file in the PYDME_HOME/archive directory,
before going to the web site to fetch it.
