Codejail plugin for `Tutor`_
============================

Tutor plugin that configures and runs a `Codejail Service`_ using a REST API. `Codejail`_ allows for the
secure execution of untrusted code within sandboxes, providing a safe environment for running potentially dangerous code.

.. _Tutor: https://docs.tutor.overhang.io
.. _Codejail Service: https://github.com/eduNEXT/codejailservice
.. _Codejail: https://github.com/openedx/codejail

Installation
------------

To install the latest version run:

.. code-block:: bash

    pip install git+https://github.com/edunext/tutor-contrib-codejail

You can install a specific version by adding the tag, branch, or commit:

.. code-block:: bash

    pip install git+https://github.com/edunext/tutor-contrib-codejail@v18.0.0

Usage
-----
Enable the plugin with:

.. code-block:: bash

    tutor plugins enable codejail

Run the initialization jobs to install the required AppArmor profile on your host:

.. code-block:: bash

    tutor config save
    tutor local do init --limit codejail

Finally, the platform can be run as usual:

.. code-block:: bash

    tutor local launch

**Please remember:** If the host is rebooted, the AppArmor profile needs to be reloaded.

Configuration
-------------

To customize the configuration, update the following settings in Tutor:

- ``CODEJAIL_APPARMOR_DOCKER_IMAGE``: (default: ``docker.io/ednxops/codejail_apparmor_loader:latest``)
- ``CODEJAIL_DOCKER_IMAGE``: (default: ``docker.io/ednxops/codejailservice:{{__version__}}``)
- ``CODEJAIL_ENFORCE_APPARMOR`` (default: ``True``)
- ``CODEJAIL_ENABLE_K8S_DAEMONSET`` (default: ``False``)
- ``CODEJAIL_SKIP_INIT`` (default: ``False``)
- ``CODEJAIL_SANDBOX_PYTHON_VERSION`` (default: ``3.8.6``)
- ``CODEJAIL_EXTRA_PIP_REQUIREMENTS`` (optional) A list of pip requirements to add to your sandbox.
- ``CODEJAIL_SERVICE_VERSION`` (default: ``release/redwood.1``),
- ``CODEJAIL_SERVICE_REPOSITORY`` (default ``https://github.com/edunext/codejailservice.git```)

.. code-block:: yaml

    CODEJAIL_EXTRA_PIP_REQUIREMENTS:
    - pybryt


Custom Image
~~~~~~~~~~~~

In most cases, you can work with the provided docker image for the release. However, you will need to re-build the docker image when:

. Additional requirements are included in the sandbox via ``CODEJAIL_EXTRA_PIP_REQUIREMENTS``.
- A different version of Python is set for the sandbox environment via ``CODEJAIL_SANDBOX_PYTHON_VERSION``.
- The custom version of edx-platform that changes the contents of requirements/edx-sandbox.

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

**NOTE**: For the Open edX version of the Lilac release, the changes required for the Codejail service to interact with ``edx-platform`` are
not included in ``open-release/lilac.master``. To use the service with the changes, please review `this PR`_.

.. _this PR: https://github.com/openedx/edx-platform/pull/27795

Kubernetes Support
------------------

The CodeJail service provides a sandbox to run arbitrary code. Security enforcement
in the sandbox is done through *AppArmor*, this means that AppArmor must be installed
in the host machine and the `provided profile`_ must be loaded.

.. _provided profile: tutorcodejail/templates/codejail/apps/profiles/docker-edx-sandbox

The plugin provides an init task running a privileged container capable of loading the AppArmor profile onto your machine.
This is only compatible with a docker installation.

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

Possible failure case
~~~~~~~~~~~~~~~~~~~~~

In case you forget to run ``tutor local do init --limit codejail`` for AppArmor profile, this error in
``Studio`` will arise::

    Error formatting HTML for the problem:
    cannot create LoncapaProblem block-v1:edX+DemoX+Demo_Course+type@problem+block@integral1: Error while
    executing script code: Codejail API Service is unavailable. Please try again in a few minutes.

.. image:: ./docs/resources/Codejailfail.png
    :width: 750px
    :align: center
    :alt: Example when codejail is not working

This indicates that the Codejail service is either not turned on or not working properly. Please ensure to follow
the steps outlined in the usage section to prevent this issue.

How to Contribute
-----------------

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/tutor-contrib-codejail/blob/main/CONTRIBUTING.rst

License
-------

This software is licensed under the terms of the AGPLv3. See the LICENSE file for details.
