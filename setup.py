from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='sga',
    ext_modules=cythonize("./*/*.pyx"),

)
