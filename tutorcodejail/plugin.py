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
        "HOST": "codejailservice.{{ LMS_HOST }}",
        "DOCKER_IMAGE": "docker.io/ednxops/codejailservice:latest",
    }
}

hooks = {
    "build-image": {"codejail": "{{ CODEJAIL_DOCKER_IMAGE }}"},
    "remote-image": {"codejail": "{{ CODEJAIL_DOCKER_IMAGE }}"},
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
