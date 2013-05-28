# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
from distutils.extension import Extension

PACKAGE_ROOT = os.path.relpath(os.path.dirname(__file__))


def get_extensions():
    sources = [os.path.join(PACKAGE_ROOT, "sofa_sidereal.pyx")]
    include_dirs = ['numpy']
    libraries = ['sofa_c']

    return [Extension(
            name="sofa_sidereal",
            sources=sources,
            include_dirs=include_dirs,
            libraries=libraries,
            language="c",)]

def get_external_libraries():
    return ['sofa']
