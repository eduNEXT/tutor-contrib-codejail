from codejail_service.settings.local import *  # pylint: disable=wildcard-import

ALLOWED_HOSTS = [
    'codejailservice',
    'localhost',
]

CODEJAIL_ENABLED = True
SECRET_KEY = '{{ CODEJAIL_SECRET_KEY }}'

CODE_JAIL = {
    'python_bin': '/sandbox/venv/bin/python',
    'user': 'sandbox',

    # Configurable limits.
    'limits': {
        # CPU-seconds
        'CPU': 3,
        # Clock seconds
        'REALTIME': 3,
        # Need at least 300 MiB memory for matplotlib alone. 512 MiB should be
        # enough headroom in general.
        'VMEM': 512 * 1024 * 1024,
        # 10 MB file size limit
        'FSIZE': 10 * 1024 * 1024,
        # 15 processes and threads (codejail default)
        'NPROC': 15,
        # Don't use a proxy process to spawn subprocesses.
        'PROXY': 0,
    },
}

{{ patch("codejail-common-settings") }}
{{ patch("codejail-production-settings") }}
