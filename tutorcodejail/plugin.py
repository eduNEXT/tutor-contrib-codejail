"""Manage the plugin for the tutorcodejail."""
from __future__ import annotations

import os
from glob import glob

import importlib_resources
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
        "SANDBOX_PYTHON_VERSION": "3.11.9",
        "SKIP_INIT": False,
        "LIMIT_CPU": "1",
        "LIMIT_MEMORY": "1Gi",
        "REQUEST_CPU": "512m",
        "REQUEST_MEMORY": "512Mi",
        "ENABLE_HPA": False,
        "MIN_REPLICAS": 1,
        "MAX_REPLICAS": 4,
        "AVG_CPU": 65,
        "SERVICE_VERSION": "release/redwood.1",
        "SERVICE_REPOSITORY": "https://github.com/edunext/codejailservice.git",
    },
    "overrides": {},
}


# To add a custom initialization task, create a bash script template under:
# tutorcodejail/templates/codejail/tasks/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...], int]] = [
    ("codejail-apparmor", ("codejail", "tasks", "codejail-apparmor", "init"), hooks.priorities.HIGH),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path, priority in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("tutorcodejail") / os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task), priority=priority)


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
    str(importlib_resources.files("tutorcodejail") / "templates")
)
# Render the "build" and "apps" folders
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("codejail/build", "plugins"),
        ("codejail/apps", "plugins"),
        ("codejail/k8s", "plugins"),
    ],
)
# Load patches from files
for path in glob(str(importlib_resources.files("tutorcodejail") / "patches" / "*")):
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
