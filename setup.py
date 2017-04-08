import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="xbox-webapi",
    version="0.0.1",
    author="tuxuser",
    author_email="no@mail.atm",
    description="A library to authenticate with Windows Live/Xbox Live and use their API",
    license="GPL",
    keywords="xbox one live api",
    url="http://packages.python.org/py-xbox-webapi",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=[
        'requests',
        'python-dateutil',
        'demjson',
        'six'
    ],
)
