PyDME: Python Bindings for Cisco DME REST API
=============================================

Documentation
-------------

PyDME is a tool to provide a simple Python abstraction over DME REST API, and managed objects.
Full documentation is available `here <https://pydme.readthedocs.io/en/latest/>`_

This tool is in pre EFT/Beta stage.

Examples
--------

Configuration and event subscription examples can be found in `examples <examples>`_ directory.

DockerFile
----------

1. Download Dockerfile located `here <https://github.com/CiscoDevNet/pydme/blob/master/Dockerfile>`_
2. Change directory to the location where the above file is downloaded.
3. ``docker build -t pydme .``
4. Once the docker image is ready, run ``docker images`` and get the IMAGE ID
5. ``docker run -it <IMAGE ID> /bin/bash``
6. Once inside the container, run ``export PYDME_HOME=/localws/pydme``
7. Change directory to ``/localws/pydme/examples``
8. Edit simpleBgpExample.py to add host, username, password of the device
9. run ``python simpleBgpExample.py``

Note: It could take a while for the docker to be installed.
