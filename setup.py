#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='envy',
    version='0.1.0-alpha',
    description='Simply create project-based work environments that your colleagues will envy',
    author='Jeremy Lucas',
    author_email='jeremyalucas@gmail.com',
    url='https://github.com/jerluc/envy',
    packages=['envy'],
    entry_points={
        'console_scripts': ['nv=envy.__main__:main', 'envy=envy.__main__:main'],
    },
    install_requires=[l.strip() for l in open('requirements.txt')],
    license='License :: OSI Approved :: Apache Software License',
)
