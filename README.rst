Codejail plugin for `Tutor`_
============================

Tutor plugin that configures and runs a `Codejail Service`_ using a REST API.
`Codejail`_ allows for the secure execution of untrusted code within sandboxes,
providing a safe environment for running potentially dangerous code.

Starting from the Ulmo release, the codejail plugin is transitioning to an
alternative implementation of the safe-exec API ( `Codejail Service V2`_).
You can opt-in to use this new implementation on Ulmo before it finally becomes
the default on the Verawood release.

.. _Tutor: https://docs.tutor.overhang.io
.. _Codejail Service: https://github.com/eduNEXT/codejailservice
.. _Codejail Service V2: https://github.com/openedx/codejail-service
.. _Codejail: https://github.com/openedx/codejail

Installation
------------

To install the latest version, run:

.. code-block:: bash

    pip install tutor-contrib-codejail
    # or install from the source
    pip install git+https://github.com/edunext/tutor-contrib-codejail

You can install a specific version by adding the tag, branch, or commit:

.. code-block:: bash

    pip install tutor-contrib-codejail~=21.0
    # or install from the source
    pip install git+https://github.com/edunext/tutor-contrib-codejail@v21.0.0

Usage
-----
Enable the plugin with:

.. code-block:: bash

    tutor plugins enable codejail

Run the initialization jobs to install the required AppArmor profile on your host:

.. code-block:: bash

    tutor config save

Finally, the platform can be run as usual:

.. code-block:: bash

    tutor local launch

**Please remember:** If the host is rebooted, the AppArmor profile needs to be reloaded.

Configuration
-------------

To customize the configuration, update the following settings in Tutor:

- ``CODEJAIL_APPARMOR_DOCKER_IMAGE``: (default: ``docker.io/ednxops/codejail_apparmor_loader:latest``)
- ``CODEJAIL_DOCKER_IMAGE_V2`` : (default: ``{{ CODEJAIL_DOCKER_IMAGE }}-v2``)
- ``CODEJAIL_DOCKER_IMAGE``: (default: ``docker.io/ednxops/codejailservice:{{__version__}}``)
- ``CODEJAIL_ENABLE_K8S_DAEMONSET`` (default: ``False``)
- ``CODEJAIL_ENFORCE_APPARMOR`` (default: ``True``)
- ``CODEJAIL_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)
- ``CODEJAIL_SANDBOX_PYTHON_VERSION`` (default: ``3.11.9``)
- ``CODEJAIL_SERVICE_REPOSITORY`` (default: ``https://github.com/edunext/codejailservice.git```)
- ``CODEJAIL_SERVICE_VERSION`` (default: ``{{ OPENEDX_COMMON_VERSION }}``),
- ``CODEJAIL_SKIP_INIT`` (default: ``False``)
- ``SERVICE_V2_REPOSITORY``: (default: ``https://github.com/openedx/codejail-service.git``)
- ``SERVICE_V2_VERSION``: (default: ``{{ OPENEDX_COMMON_VERSION }}``)
- ``USE_SERVICE_V2``: (default: ``False``)

The ``CODEJAIL_V2_*`` settings are meant to be used only during the Ulmo
release and will be phased-out during the Verawood release.

To opt-in to the new implementation of the code-exec API set ``USE_SERVICE_V2``
to ``True`` and re-deploy your environment. If you are using a a custom image
for the codejail service you will need to rebuild it with ``USE_SERVICE_V2``
set to ``True``.

Custom Image
~~~~~~~~~~~~

In most cases, you can work with the provided Docker image for the release. However, you will need to rebuild the Docker image when:

. Additional requirements are included in the sandbox via ``CODEJAIL_EXTRA_PIP_REQUIREMENTS``.
- A different version of Python is set for the sandbox environment via ``CODEJAIL_SANDBOX_PYTHON_VERSION``.
- You are using a custom version of edx-platform that changes the contents of requirements/edx-sandbox.

Create a new image running:

.. code-block:: bash

    # Add the tutor configuration with the custom value
    tutor config save \
    --set 'CODEJAIL_EXTRA_PIP_REQUIREMENTS=["pybryt"]'

    # Build the image
    tutor images build codejail


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
| Redwood          | >= 18.x       |
+------------------+---------------+
| Sumac            | >= 19.x       |
+------------------+---------------+
| Teak             | >= 20.x       |
+------------------+---------------+
| Ulmo             | >= 21.x       |
+------------------+---------------+

**NOTE**: For the Open edX version of the Lilac release, the changes required for the Codejail service to interact with ``edx-platform`` are
not included in ``open-release/lilac.master``. To use the service with the changes, please review `this PR`_.

.. _this PR: https://github.com/openedx/edx-platform/pull/27795

Kubernetes Support
------------------

The CodeJail service provides a sandbox to run arbitrary code. Security enforcement
in the sandbox is done through *AppArmor*, this means that AppArmor must be installed
in the host machine, and the `provided profile`_ must be loaded.

.. _provided profile: tutorcodejail/templates/codejail/apps/profiles/docker-edx-sandbox

The plugin provides an init task running a privileged container capable of loading the AppArmor profile onto your machine.
This is only compatible with a Docker installation.

For Kubernetes environments, ensure each node has AppArmor installed and the profile loaded. Optionally,
set ``CODEJAIL_ENABLE_K8S_DAEMONSET`` to True to use a DaemonSet for loading the AppArmor profile,
assuming the nodes are already running AppArmor.

If you choose to run the service without enforcing the AppArmor profile, you can set ``CODEJAIL_ENFORCE_APPARMOR`` to ``False``.

More info about this discussion can be found on `this issue`_.

.. _this issue: https://github.com/eduNEXT/tutor-contrib-codejail/issues/24

Testing Functionality
---------------------

To verify if Codejail is working, use a course with loncapa problems in ``Studio`` and check for correct execution.
You can import the provided `example course`_.

Once the course is imported, go to any section and select an exercise (`section example`_), the proper result is:

.. _example course: https://github.com/eduNEXT/tutor-contrib-codejail/blob/main/docs/resources/course_codejail_example.tar.gz
.. _section example: http://studio.local.overhang.io:8001/container/block-v1:edX+DemoX+Demo_Course+type@vertical+block@v-integral1

.. image:: ./docs/resources/Codejailworking.png
    :width: 725px
    :align: center
    :alt: Example when codejail is working

In this case, the section's content will render correctly and work as specified in the instructions of the problem.

How to Contribute
-----------------

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/tutor-contrib-codejail/blob/main/CONTRIBUTING.rst

License
-------

This software is licensed under the terms of the AGPLv3. See the LICENSE file for details.
