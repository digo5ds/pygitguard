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
            "pygitguard=pygitguard.cli:main",
        ],
    },
)
