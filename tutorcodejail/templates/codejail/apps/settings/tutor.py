from .base import *

from codejail.django_integration_utils import apply_django_settings

SECRET_KEY = "{{ CODEJAIL_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "{{ CODEJAIL_HOST }}",
]

#################### Python sandbox ############################################

CODE_JAIL = {
    'python_bin': '/sandbox/venv/bin/python',
    # User to run as in the sandbox.
    'user': 'sandbox',

    # Configurable limits.
    # Setting all of them to 0 to disable limits in conatiners.
    'limits': {
        #
    	'NPROC': 0,
        # How many CPU seconds can jailed code use?
        'CPU': 0,
        # Limit the memory of the jailed process to something high but not
        # infinite (512MiB in bytes)
        'VMEM': 0,
        # Time in seconds that the jailed process has to run.
        'REALTIME': 0,
        # Needs to be non-zero so that jailed code can use it as their temp directory.(10MiB in bytes)
        'FSIZE': 10485760,
        # Disable usage of proxy (force thread-safe)
        'PROXY': 0,
    },

    # Overrides to default configurable 'limits' (above).
    # Keys should be course run ids.
    # Values should be dictionaries that look like 'limits'.
    "limit_overrides": {},
}

apply_django_settings(CODE_JAIL)
