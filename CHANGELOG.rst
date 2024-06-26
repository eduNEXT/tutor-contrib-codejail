Change Log
==========

..
   All enhancements and patches to api_contracts will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

[18.0.0] - 2024-06-26
~~~~~~~~~~~~~~~~~~~~~
* feat: redwood support

  Add two new variables to enable the use of custom versions/forks of
  `edunext/codejailservice`.

  BREAKING CHANGE: the default Python version of the sandbox environment
  has been bumped to 3.11. This change alongside the upgrade of the SciPy
  and NumPy dependencies may cause some instructor code to fail.

[17.0.2] - 2024-05-24
~~~~~~~~~~~~~~~~~~~~~
* fix: use tutor config on codejail service and add patches to edit it DS-894 (#55)

[17.0.1] - 2023-11-20
~~~~~~~~~~~~~~~~~~~~~

* fix: remove deprecated is_buildkit_enabled which now always evaluates to 'true' (#47)


[17.0.0] - 2023-11-20
~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Allows you to add extra pip requirements to your codejail sandbox (#42)
* Add support form quince release (#43)

[16.0.0] - 2023-08-18
~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add support for palm release (#39)

[15.2.0] - 2023-07-14
~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add hpa and resources limits (#37)

[15.1.0] - 2023-05-25
~~~~~~~~~~~~~~~~~~~~

Added
_____

* Update readme following latest changes (#34)
* Allow to use tmp in python executions.

[15.0.0] - 2023-01-12
~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add support for Olive release (#28).
* Adds mantainer group.

[14.1.0] - 2022-09-26
~~~~~~~~~~~~~~~~~~~~

Added
-----
* Include k8s templates.
* Add a setting to run the service without codejail.
* Add a setting to skip the initialization job.
* Add a section in the readme with the available configuration values and their defaults.


[14.0.0] - 2022-05-30
~~~~~~~~~~~~~~~~~~~~

Added
_____

* Bump version according tutor practices for Nutmeg release.

[13.0.0] - 2022-05-02
~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add repo documentation.
* Bump version according tutor practices for Maple release.

[12.0.2] - 2022-04-29
~~~~~~~~~~~~~~~~~~~~

Added
_____

* First git tagged release
* Add quality tests to maintain the repo
* Add requirements files.
* Add Add required maintenance files.
