from setuptools import find_packages, setup

pkgs = find_packages("src")

name = pkgs[0]

setup(
    entry_points={
        "console_scripts": [
            f"{name}={name}.__main__:api.format",
        ],
    },
    install_requires=[
        "pyparsing==3.0.7",
    ],
    name=name,
    packages=pkgs,
    package_dir={"": "src"},
)
