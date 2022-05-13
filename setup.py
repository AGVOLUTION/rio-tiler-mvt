"""Setup for rio-tiler-mvt."""

from setuptools.extension import Extension
from setuptools import setup, find_packages
from Cython.Build import cythonize
import os

import numpy


with open("README.md") as f:
    long_description = f.read()

# vtzero = "vtzero @ git+https://github.com/schneidemar/python-vtzero.git@d85a55387a15c69b149915beab8ce738ed3de0e3#egg=vtzero"
vtzero = "vtzero @ git+https://github.com/AGVOLUTION/python-vtzero.git@bc48b6d4fb36c5ea387710203cda78b1cd53b100#egg=vtzero"
# vtzero = f"vtzero @ file://localhost/{os.getcwd()}/../python-vtzero#egg=vtzero"

inst_reqs = ["numpy", vtzero, "Cython"]

vt = "vector-tile-base @ git+https://github.com/mapbox/vector-tile-base.git"
rio_tiler = "rio-tiler==1.4.0"
extra_reqs = {
    "test": [vt, rio_tiler, "pytest", "pytest-cov"],
    "dev": [vt, rio_tiler, "pytest", "pytest-cov", "pre-commit"],
}

ext_options = {"include_dirs": [numpy.get_include()]}
ext_modules = cythonize(
    [Extension("rio_tiler_mvt.mvt", ["rio_tiler_mvt/mvt.pyx"], **ext_options)],
    language_level="3",
)

setup(
    name="rio-tiler-mvt",
    version="0.0.3",
    description=u"""A rio-tiler plugin to encode tile array to MVT""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="COG MVT mapbox vectortile GIS",
    author=u"Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/cogeotiff/rio-tiler-mvt",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    ext_modules=ext_modules,
)
