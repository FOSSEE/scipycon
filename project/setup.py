
from setuptools import setup

setup(
    name='project',
    version='1.0',
    description="SciPy.in Conference django website",
    entry_points={
        "console_scripts": [
            'initdb = scripts.initdb:main',
        ]
    },
)

