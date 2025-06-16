from setuptools import find_packages, setup

setup(
    name="pygitguard",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pygitguard=pygitguard_cli:main",
        ],
    },
)
