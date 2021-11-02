"""Manage the plugin for the tutorcodejail."""

import os
from glob import glob

import pkg_resources
from .__about__ import __version__

templates = pkg_resources.resource_filename("tutorcodejail", "templates")

config = {
    "add": {
        "SECRET_KEY": "{{ 24|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "HOST": "codejailservice",
        "DOCKER_IMAGE": f"docker.io/ednxops/codejailservice:{__version__}",
        "SANDBOX_PYTHON_VERSION": "3.5.10",
    },
    "set": {},
}

hooks = {
    "build-image": {
        "codejail": "{{ CODEJAIL_DOCKER_IMAGE }}",
        "codejail_apparmor": f"docker.io/ednxops/codejail_apparmor:{__version__}",
    },
    "remote-image": {
        "codejail": "{{ CODEJAIL_DOCKER_IMAGE }}",
        "codejail_apparmor": f"docker.io/ednxops/codejail_apparmor:{__version__}",
    },
    "init": ["codejail_apparmor"],
}


def patches():
    """Logic for retrueve all the patches of tutorcodejail."""
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("tutorcodejail", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path, encoding="utf-8") as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
