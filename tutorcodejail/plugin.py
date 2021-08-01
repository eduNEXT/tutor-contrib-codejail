from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename(
    "tutorcodejail", "templates"
)

config = {
    "add": {
        "SECRET_KEY": "{{ 24|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "HOST": "codejailservice",
        "DOCKER_IMAGE": "docker.io/ednxops/codejailservice:latest",
    },
    "set":{
        "SANDBOX_PYTHON_VERSION": "3.5.10",
    }
}

hooks = {
    "build-image": {
        "codejail": "{{ CODEJAIL_DOCKER_IMAGE }}",
        "codejail_apparmor": "docker.io/ednxops/codejail_apparmor:latest"
    },
    "remote-image": {
        "codejail": "{{ CODEJAIL_DOCKER_IMAGE }}",
        "codejail_apparmor": "docker.io/ednxops/codejail_apparmor:latest"
    },
    "init": ["codejail_apparmor"]
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename(
        "tutorcodejail", "patches"
    )
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
