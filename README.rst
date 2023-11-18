Codejail plugin for `Tutor`_
============================

Tutor plugin that enables execution of untrusted code in secure sandboxes using an external `service`_ based on the `codejail`_ library.

.. _Tutor: https://docs.tutor.overhang.io
.. _service: https://github.com/eduNEXT/codejailservice
.. _codejail: https://github.com/openedx/codejail

Installation
------------

.. code-block:: bash

    pip install git+https://github.com/edunext/tutor-contrib-codejail

Usage
-----

.. code-block:: bash

    tutor plugins enable codejail

Then, you will have to install the "docker-edx-sandbox" apparmor profile on your host:

.. code-block:: bash

    tutor config save
    tutor local do init --limit codejail

Finally, the platform can be run as usual:

.. code-block:: bash

    tutor local launch

Configuration
-------------

For some of these configurations to work correctly, the codejail image must be built again. Command to build codejail: ``tutor images build codejail``.

- ``CODEJAIL_APPARMOR_DOCKER_IMAGE``: (default: ``docker.io/ednxops/codejail_apparmor_loader:latest``)
- ``CODEJAIL_DOCKER_IMAGE``: (default: ``docker.io/ednxops/codejailservice:14.0.0``)
- ``CODEJAIL_ENFORCE_APPARMOR`` (default: ``True``)
- ``CODEJAIL_ENABLE_K8S_DAEMONSET`` (default: ``False``)
- ``CODEJAIL_SKIP_INIT`` (default: ``False``)
- ``CODEJAIL_SANDBOX_PYTHON_VERSION`` (default: ``3.8.6``)
- ``CODEJAIL_EXTRA_PIP_REQUIREMENTS`` (optional) A list of pip requirements to add to your sandbox.
    
    .. code-block:: yaml

        CODEJAIL_EXTRA_PIP_REQUIREMENTS:
        - pybryt


Compatibility
-------------

+------------------+---------------+
| Open edX Release | Tutor Version |
+==================+===============+
| Lilac            | >= 12.x       |
+------------------+---------------+
| Maple            | >= 13.x       |
+------------------+---------------+
| Nutmeg           | >= 14.x       |
+------------------+---------------+
| Olive            | >= 15.x       |
+------------------+---------------+
| Palm             | >= 16.x       |
+------------------+---------------+
| Quince           | >= 17.x       |
+------------------+---------------+

**NOTE**: For the Open edx version of the Lilac release, the changes required for the Codejail service to interact with ``edx-platform`` are
not included in ``open-release/lilac.master``. In order to use the service with the changes, please review `this PR`_.

.. _this PR: https://github.com/openedx/edx-platform/pull/27795

Kubernetes Support
------------------

The CodeJail service provides a sandbox to run arbitrary code. Security enforcement
in the sandbox is done through AppArmor, this means that AppArmor must be installed
in the host machine and the `provided profile`_ must be loaded.

.. _provided profile: tutorcodejail/templates/codejail/apps/profiles/docker-edx-sandbox

The plugin provides an init task that runs a privileged container capable of loading
the needed AppArmor profile unto your machine. This is only compatible with a docker
installation. In Kubernetes you must guarantee that each node of your cluster has
AppArmor installed and the profile loaded, for that reason the one time initialization
task that is used in the init is skipped when running on kubernetes.

The plugins offers the possibility to load the AppArmor profile using a DaemonSet,
assuming the nodes are already running AppArmor. To do so you must set
``CODEJAIL_ENABLE_K8S_DAEMONSET`` to ``True``.

If, at your own discretion, want to run the service without enforcing the AppArmor
profile you can set ``CODEJAIL_ENFORCE_APPARMOR`` to ``False``.

More info about this discussion can be found on `this issue`_.

.. _this issue: https://github.com/eduNEXT/tutor-contrib-codejail/issues/24

Functionality test
------------------

How to know if codejail is working
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to test whether codejail is working is to validate it in ``Studio`` with a course
that has loncapa problems.

This test was performed on the Maple version of Open edx, using the course ``course_codejail_example.tar.gz``
found in the additional resources section.

Once the course is imported, go to any section and select an exercise (`section example`_), the proper result is:

.. _section example: http://studio.local.overhang.io:8001/container/block-v1:edX+DemoX+Demo_Course+type@vertical+block@v-integral1

.. image:: ./docs/resources/Codejailworking.png
    :width: 725px
    :align: center
    :alt: Example when codejail is working

In this case, the section's content will render correctly and will be working as specified in the instructions of the problem.

Possible failure case
~~~~~~~~~~~~~~~~~~~~~

In case you forget to run ``tutor local do init --limit codejail`` for apparmor profile, this error in
``Studio`` will arise::

    Error formatting HTML for problem:
    cannot create LoncapaProblem block-v1:edX+DemoX+Demo_Course+type@problem+block@integral1: Error while
    executing script code: Codejail API Service is unavailable. Please try again in a few minutes.

.. image:: ./docs/resources/Codejailfail.png
    :width: 750px
    :align: center
    :alt: Example when codejail is not working

This indicates that the codejail service is not turned on or is not working properly. Be sure to follow the
steps in the usage section so this doesn't happen.

Additional Resources
--------------------

Example course to test the Codejail service: `course_codejail_example.tar.gz`_

.. _course_codejail_example.tar.gz: https://github.com/eduNEXT/tutor-contrib-codejail/blob/main/docs/resources/course_codejail_example.tar.gz

How to Contribute
-----------------

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/tutor-contrib-codejail/blob/main/CONTRIBUTING.rst

License
-------

This software is licensed under the terms of the AGPLv3.
