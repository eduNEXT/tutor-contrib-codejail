Purpose of this Repo
=======================

Status
------

Accepted

Context
-------

Tutor plugin is required for the installation of the codejail service in some Open edx releases with tutor,
because it makes it easier to implement the service without the need to touch code on the edx platform.

Decision
--------

Create a tutor-contrib-plugin that facilitates the installation of the codejail service, using tutor commands
that pull Docker images and create the container where the service runs, independent of the platform's own containers.

Consequences
------------

The creation of this plugin affects the installation and operation of the codejail service, adapting the necessary instances
so that it works according to the service specifications.
