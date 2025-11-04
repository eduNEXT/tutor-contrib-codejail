"""Manage the plugin for the tutorcodejail."""

from __future__ import annotations

import os
import typing as t
from glob import glob
from pathlib import Path

import importlib_resources
from tutor import hooks
from tutor.types import Config

from .__about__ import __version__

ABI_PATH = "/etc/apparmor.d/abi"

config = {
    "unique": {
        "SECRET_KEY": "{{ 24|random_string }}",
    },
    "defaults": {
        "APPARMOR_DOCKER_IMAGE": "docker.io/ednxops/codejail_apparmor_loader:apparmor-4",
        "DOCKER_IMAGE": f"docker.io/ednxops/codejailservice:{__version__}",
        "DOCKER_IMAGE_V2": "{{ CODEJAIL_DOCKER_IMAGE }}-v2",
        "ENABLE_K8S_DAEMONSET": False,
        "ENFORCE_APPARMOR": True,
        "EXTRA_PIP_REQUIREMENTS": [],
        "HOST": "codejailservice",
        "SANDBOX_PYTHON_VERSION": "3.11.14",
        "SERVICE_REPOSITORY": "https://github.com/edunext/codejailservice.git",
        "SERVICE_V2_REPOSITORY": "https://github.com/openedx/codejail-service.git",
        "SERVICE_V2_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "SERVICE_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "SKIP_INIT": False,
        "USE_SERVICE_V2": False,
        "VERSION": __version__,
    },
    "overrides": {},
}


def get_apparmor_abi():
    """
    Return the latest default abi rule if available in the system.

    AppArmor uses the Policy feature ABI to establish which rules it can
    enforce based on the kernel capabilities. AppArmor profiles can include an
    ABI rule to indicate the ABI they were developed under. If no rule is used
    AppArmor will fallback to whichever rule is pinned in the
    `/etc/apparmor/parser.conf` file.

    We try to use at least the 3.0 abi whenever it's available at `/etc/apparmor.d/abi/`
    to guarantee that network rules are correctly enforced on newer versions of
    the kernel. If neither the 3.0 ABI nor the 4.0 ABI are present we don't set
    the abi rule and instead rely on the default fallback.

    See: https://github.com/netblue30/firejail/issues/3659#issuecomment-711074899
    """
    if Path(f"{ABI_PATH}/4.0").exists():
        return "abi <abi/4.0>,"

    if Path(f"{ABI_PATH}/3.0").exists():
        return "abi <abi/3.0>,"

    return ""


hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [
        ("get_apparmor_abi", get_apparmor_abi()),
    ]
)


@hooks.Filters.IMAGES_BUILD.add()
def _build_codejail_images(
    images: list[tuple[str, t.Union[str, tuple[str, ...]], str, tuple[str, ...]]],
    tutor_config: Config,
):
    """Choose the appropiate build context when using CODEJAIL_USE_SERVICE_V2."""
    # TODO: Remove after the Verawood update
    if tutor_config.get("CODEJAIL_USE_SERVICE_V2"):
        codejail_img = (
            "codejail",
            "plugins/codejail/build/codejail-service",
            "{{ CODEJAIL_DOCKER_IMAGE_V2 }}",
            (),
        )
    else:
        codejail_img = (
            "codejail",
            "plugins/codejail/build/codejail",
            "{{ CODEJAIL_DOCKER_IMAGE }}",
            (),
        )
    apparmor_img = (
        "codejail_apparmor",
        ("plugins", "codejail", "build", "codejail_apparmor"),
        "{{CODEJAIL_APPARMOR_DOCKER_IMAGE}}",
        (),
    )

    return images + [codejail_img, apparmor_img]


@hooks.Filters.IMAGES_PUSH.add()
def _push_codejail_images(
    images: list[tuple[str, t.Union[str, tuple[str, ...]], str, tuple[str, ...]]],
    tutor_config: Config,
):
    """Choose the appropiate image tag when using CODEJAIL_USE_SERVICE_V2."""
    # TODO: Remove after the Verawood update
    if tutor_config.get("CODEJAIL_USE_SERVICE_V2"):
        codejail_img = (
            "codejail",
            "{{ CODEJAIL_DOCKER_IMAGE_V2 }}",
        )
    else:
        codejail_img = (
            "codejail",
            "{{ CODEJAIL_DOCKER_IMAGE }}",
        )
    apparmor_img = (
        "codejail_apparmor",
        "{{CODEJAIL_APPARMOR_DOCKER_IMAGE}}",
    )
    return images + [codejail_img, apparmor_img]


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
    [(f"CODEJAIL_{key}", value) for key, value in config.get("defaults", {}).items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"CODEJAIL_{key}", value) for key, value in config.get("unique", {}).items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
