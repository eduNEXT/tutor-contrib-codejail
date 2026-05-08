# ChangeLog

<!--
All enhancements and changes will be documented in this file.  It adheres to
the structure of http://keepachangelog.com/ ,

This project adheres to Semantic Versioning (http://semver.org/).
-->

## Unreleased

See the fragment files in the [changelog.d/ directory](./changelog.d).

<!-- scriv-insert-here -->

<a id='changelog-21.0.1'></a>
## 21.0.1 — 2026-05-08

### Fixed

- Properly wait for apparmor_loader container to run before spawning
  codejailservice container.

<a id='changelog-21.0.0'></a>
## 21.0.0 - 2025-11-04

- feat!: add support for the Ulmo release
 
  This changes also include support for openedx/codejail-service as an
  alternative implementation of the safe_exec REST API.

## 20.1.0 - 2025-11-25

- feat!: remove autoscaling configuration and apply miscellaneous fixes (#73)

  The autoscaling configuration has long been unmaintained and should be
  instead handled by https://github.com/eduNEXT/tutor-contrib-pod-autoscaling.

  The variable used to install extra packages in the sandbox virtual
  environment was not properly configured as a default variable.

  The apparmor-loader deamon set was not using the same image as the
  docker deployment, and the generated config-maps where missing
  appropriate labels.

- feat: use an "init service" to load the apparmor profile (#63)
 
  This follows the same logic as the "permissions" service used by tutor
  core. The `codejail-apparmor-loader` service runs the command used
  previously by the init job.
 
  It makes more sense to handling loading of the apparmor profile with an
  init service:
 
  - The profile is ephemeral, rebooting the host will require to load it
    again.
  - The profile is a dependency for the container to start. Things like
    database migrations, which are the main use case for init jobs, don't
    block the start of the main service container.

## 20.0.0 - 2025-06-27

- feat: teak support

## 19.1.1 - 2025-04-07

- fix: set FLASK_APP_SETTINGS env for k8s-deployment (#65)

## 19.1.0 - 2025-02-21

- feat: update to sumac.2

## 19.0.0 - 2024-12-17

- feat: sumac upgrade

  Adjust the globing and abi rules in the apparmor profile:

  Newer versions of ubuntu (>24.04) do not pin the AppArmor Policy feature
  ABI which causes certain rules to not be enforced. We include an abi
  rule to use the relatively common 3.0 policy whenever it's available in
  the system, if it's not available we rely on the default fallback
  behaviour. The 3.0 policy should be present on any system using
  AppArmor>3.x (e.g. Ubuntu 22.04 or newer).

  The globbing rules in the profile were adjusted to cover a larger range
  of python versions and avoid creating new profiles for different
  versions of python used by the sandbox environment.

  To load the profile we need at least AppArmor 3.0, to avoid confusion in
  the future we pin the alpine base image and define a proper tag for the
  apparmorloader image.


## 18.0.0 - 2024-06-26

- feat: redwood support

  Add two new variables to enable the use of custom versions/forks of
  [edunext/codejailservice]{.title-ref}.

  BREAKING CHANGE: the default Python version of the sandbox environment
  has been bumped to 3.11. This change alongside the upgrade of the
  SciPy and NumPy dependencies may cause some instructor code to fail.

## 17.0.2 - 2024-05-24

- fix: use tutor config on codejail service and add patches to edit it
  DS-894 (#55)

## 17.0.1 - 2023-11-20

- fix: remove deprecated is_buildkit_enabled which now always evaluates
  to 'true' (#47)

## 17.0.0 - 2023-11-20

### Added

- Allows you to add extra pip requirements to your codejail sandbox
  (#42)
- Add support form quince release (#43)

## 16.0.0 - 2023-08-18

### Added

- Add support for palm release (#39)

## 15.2.0 - 2023-07-14

### Added

- Add hpa and resources limits (#37)

## 15.1.0 - 2023-05-25

### Added

- Update readme following latest changes (#34)
- Allow to use tmp in python executions.

## 15.0.0 - 2023-01-12

### Added

- Add support for Olive release (#28).
- Adds mantainer group.

## 14.1.0 - 2022-09-26 

### Added

- Include k8s templates.
- Add a setting to run the service without codejail.
- Add a setting to skip the initialization job.
- Add a section in the readme with the available configuration values
  and their defaults.

## 14.0.0 - 2022-05-30

### Added

- Bump version according tutor practices for Nutmeg release.

## 13.0.0 - 2022-05-02 

### Added

- Add repo documentation.
- Bump version according tutor practices for Maple release.

## 12.0.2 - 2022-04-29 

### Added

- First git tagged release
- Add quality tests to maintain the repo
- Add requirements files.
- Add Add required maintenance files.
