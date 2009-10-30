
from setuptools import setup

setup(
    name='project',
    version='1.0',
    description="KiwiPyCon django website",
    entry_points={
        "console_scripts": [
            'initdb = scripts.initdb:main',
        ]
    },
)

