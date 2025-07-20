from setuptools import find_packages, setup

from pygitguard.__version__ import get_version

setup(
    name="pygitguard",
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pygitguard=pygitguard.cli:main ",
        ],
    },
    author="Diogo Ferreira da Silva",
    description="A Git security scanner that detects and prevents accidental commits of secrets, credentials, and other sensitive information during development.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/digo5ds/pygitguard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
