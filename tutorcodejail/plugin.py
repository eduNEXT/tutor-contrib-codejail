"""Manage the plugin for the tutorcodejail."""
from __future__ import annotations

import os
from glob import glob
from pathlib import Path

import importlib_resources
from tutor import hooks

from .__about__ import __version__

ABI_PATH = "/etc/apparmor.d/abi"

config = {
    "unique": {
        "SECRET_KEY": "{{ 24|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "APPARMOR_DOCKER_IMAGE": "docker.io/ednxops/codejail_apparmor_loader:apparmor-3",
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
        "SERVICE_VERSION": "release/sumac.1",
        "SERVICE_REPOSITORY": "https://github.com/edunext/codejailservice.git",
    },
    "overrides": {},
}


def get_apparmor_abi():
    """
    Return the default abi 3.0 rule if available in the system.

    AppArmor uses the Policy feature ABI to establish which rules it can
    enforce based on the kernel capabilities. AppArmor profiles can include an
    ABI rule to indicate the ABI they were developed under. If no rule is used
    AppArmor will fallback to whichever rule is pinned in the
    `/etc/apparmor/parser.conf` file.

    We try to use the 3.0 abi whenever it's available at `/etc/apparmor.d/abi/`
    to guarantee that network rules are correctly enforced on newer versions of
    the kernel. If the ABI is not present we don't set the abi rule and instead
    rely on the default fallback.

    See: https://github.com/netblue30/firejail/issues/3659#issuecomment-711074899
    """
    if Path(f"{ABI_PATH}/3.0").exists():
        return "abi <abi/3.0>,"
    return ""


hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [
        ("get_apparmor_abi", get_apparmor_abi()),
    ]
)

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
