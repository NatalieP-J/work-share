# compile sofa stuff with python setup.py build_ext --inplace

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

def get_extensions():
    sources = ["sofa_sidereal.pyx"]
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

setup(name='sidereal', 
      cmdclass = {'build_ext': build_ext},
      ext_modules=get_extensions())

