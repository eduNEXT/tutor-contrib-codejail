codejail plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/edunext/tutor-contrib-codejail

Usage
-----

::

    tutor plugins enable codejail

Then, you will have to install the "docker-edx-sandbox" apparmor profile on your host::

    tutor config save
    tutor local init --limit=codejail

Finally, the platform can be run as usual::

    tutor local quickstart

License
-------

This software is licensed under the terms of the AGPLv3.
