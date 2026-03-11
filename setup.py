from setuptools import setup, Extension
import pybind11

ext_module = Extension(
    'queue_stl_pybind',
    sources=['queue_stl_pybind.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=['-std=c++11', '-O3', '-Wall'],
)

setup(
    name='queue_stl_pybind',
    version='1.0',
    description='Очередь на STL через pybind11',
    ext_modules=[ext_module],
)