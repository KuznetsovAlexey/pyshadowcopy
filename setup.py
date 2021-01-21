from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pyshadowcopy',
    version='0.0.1',
    description='A wrapper over the WMI Win32_ShadowCopy class for Python',
    long_description=long_description,
    url='https://github.com/KuznetsovAlexey/pyshadowcopy',
    author='KuznetsovAlexey',
    license='MIT',
    keywords=['Windows', 'Shadow Copy', 'win32'],
    py_modules=['pyshadowcopy'],
    install_requires=['pypiwin32', 'wmi'],
)