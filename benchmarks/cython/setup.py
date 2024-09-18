from setuptools import setup
from Cython.Build import cythonize

setup(
    name = 'bigproduct.app',
    ext_modules=cythonize("bigproduct.pyx"),
)

setup(
    name = 'bigproduct2.app',
    ext_modules=cythonize("bigproduct2.pyx"),
)
