"""Manage the plugin for the tutorcodejail."""

import os
from glob import glob

import pkg_resources
from tutor import hooks

from .__about__ import __version__

config = {
    "unique": {
        "SECRET_KEY": "{{ 24|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "APPARMOR_DOCKER_IMAGE": "docker.io/ednxops/codejail_apparmor_loader:latest",
        "DOCKER_IMAGE": f"docker.io/ednxops/codejailservice:{__version__}",
        "ENABLE_K8S_DAEMONSET": False,
        "ENFORCE_APPARMOR": True,
        "HOST": "codejailservice",
        "SANDBOX_PYTHON_VERSION": "3.8.6",
        "SKIP_INIT": False,
        "LIMIT_CPU": "1",
        "LIMIT_MEMORY": "1Gi",
        "REQUEST_CPU": "512m",
        "REQUEST_MEMORY": "512Mi",
        "ENABLE_HPA": False,
        "HPA_MIN_REPLICAS": 1,
        "HPA_MAX_REPLICAS": 4,
        "AVG_CPU": 65,
        "AVG_MEMORY": 65
    },
    "overrides": {},
}


hooks.Filters.COMMANDS_INIT.add_item((
    "codejail-apparmor",
    ("codejail", "tasks", "codejail-apparmor", "init"),
))


hooks.Filters.IMAGES_BUILD.add_item((
    "codejail",
    ("plugins", "codejail", "build", "codejail"),
    "{{ CODEJAIL_DOCKER_IMAGE }}",
    (),
))


hooks.Filters.IMAGES_BUILD.add_item((
    "codejail_apparmor",
    ("plugins", "codejail", "build", "codejail_apparmor"),
    "{{CODEJAIL_APPARMOR_DOCKER_IMAGE}}",
    (),
))


hooks.Filters.IMAGES_PULL.add_item((
    "codejail",
    "{{ CODEJAIL_DOCKER_IMAGE }}",
))


hooks.Filters.IMAGES_PULL.add_item((
    "codejail_apparmor",
    "{{CODEJAIL_APPARMOR_DOCKER_IMAGE}}",
))


hooks.Filters.IMAGES_PUSH.add_item((
    "codejail",
    "{{ CODEJAIL_DOCKER_IMAGE }}",
))


hooks.Filters.IMAGES_PUSH.add_item((
    "codejail_apparmor",
    "{{CODEJAIL_APPARMOR_DOCKER_IMAGE}}",
))


# Boilerplate code
# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorcodejail", "templates")
)
# Render the "build" and "apps" folders
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("codejail/build", "plugins"),
        ("codejail/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorcodejail", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
# Add configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"CODEJAIL_{key}", value)
        for key, value in config.get("defaults", {}).items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"CODEJAIL_{key}", value)
        for key, value in config.get("unique", {}).items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
