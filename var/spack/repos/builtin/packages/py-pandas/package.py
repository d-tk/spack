from spack import *
import os

class PyPandas(Package):
    """pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with relational or labeled data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, real world data analysis in Python. Additionally, it has the broader goal of becoming the most powerful and flexible open source data analysis / manipulation tool available in any language."""
    homepage = "http://pandas.pydata.org/"
    url      = "https://pypi.python.org/packages/source/p/pandas/pandas-0.16.0.tar.gz#md5=bfe311f05dc0c351f8955fbd1e296e73"

    version('0.16.0', 'bfe311f05dc0c351f8955fbd1e296e73')
    version('0.16.1', 'fac4f25748f9610a3e00e765474bdea8')
    version('0.18.0', 'f143762cd7a59815e348adf4308d2cf6')

    extends('python', ignore=r'bin/f2py$')
    depends_on('py-dateutil')
    depends_on('py-numpy')
    depends_on('py-setuptools')
    depends_on('py-pytz')
    depends_on('py-numexpr')
    depends_on('py-bottleneck')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
