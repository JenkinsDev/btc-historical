import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "btc_historical",
    version = "0.1.0",
    author = "David Jenkins",
    author_email = "david.nicholas.jenkins@gmail.com",
    description = ("CLI Tool & Library For Retrieving "
                   "Historical BTC Pricing Data"),
    license = "MIT",
    keywords = "bitcoin btc pricing historic",
    url = "https://github.com/JenkinsDev/btc-history",
    packages=['historical', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ]
)
