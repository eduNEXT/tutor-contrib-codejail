"""Setup configuration for the tutorcodejail."""

import io
import os

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    """Read the README.rst file."""
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as file:
        return file.read()


def load_about():
    """Read the about entry of tutorcodejail."""
    about = {}
    with io.open(
        os.path.join(HERE, "tutorcodejail", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as file:
        exec(file.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-codejail",
    version=ABOUT["__version__"],
    url="https://github.com/github/tutor-contrib-codejail",
    project_urls={
        "Code": "https://github.com/edunext/tutor-contrib-codejail",
        "Issue tracker": "https://github.com/edunext/tutor-contrib-codejail/issues",
    },
    license="AGPLv3",
    author="Eric Herrera",
    description="codejail plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=["tutor"],
    entry_points={"tutor.plugin.v1": ["codejail = tutorcodejail.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
