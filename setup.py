"""Setup for pypetwalk python package."""
from __future__ import annotations

from os import path

from setuptools import find_packages, setup

PACKAGE_NAME = "pypetwalk"
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

VERSION = {}
# pylint: disable=exec-used
with open(path.join(HERE, PACKAGE_NAME, "__version__.py"), encoding="utf-8") as fp:
    exec(fp.read(), VERSION)

PACKAGES = find_packages(exclude=["tests", "tests.*", "dist", "build"])

REQUIRES = ["aiohttp>=3.8.1"]

setup(
    name=PACKAGE_NAME,
    version=VERSION["__version__"],
    license="MIT License",
    url="https://github.com/p0l0/pypetwalk",
    download_url="https://github.com/p0l0/pypetwalk/tarball/" + VERSION["__version__"],
    author="Marco Neumann",
    author_email="pypetwalk@binware.dev",
    description="Python library to communicate with the petWALK.control module",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=PACKAGES,
    package_data={"pypetwalk": ["py.typed"]},
    zip_safe=False,
    platforms="any",
    python_requires=">=3.9",
    install_requires=REQUIRES,
    keywords=["petwalk", "petwalk.control", "home", "automation"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
    ],
)
