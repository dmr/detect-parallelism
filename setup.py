#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='detect-parallelism',
    version='0.1',
    url='https://github.com/dmr/detect-parallelism',
    license='MIT',
    author='Daniel Rech',
    author_email='danielmrech@gmail.com',
    description=(
        'Tries different implementations to query many urls and detects '
        'the optimal implementation and the possible parallelism of the '
        'internet connection and the hardware used'
        ),
    py_modules= ['detect_parallelism',
                 'detect_parallelism_graph'],
    entry_points={
        'console_scripts': [
            'detect_parallelism = detect_parallelism:main',
            'detect_parallelism_graph = detect_parallelism_graph:main'
        ],
    },

    dependency_links = [
        'https://github.com/dmr/query-model/tarball/master#egg=query_model-1.0.1',
    ],

    install_requires=[
        'argparse',
        'pycurl',
        'pandas',
        'numpy',
        'matplotlib',
        #statsmodels #optional
        'query_model>=1.0.1',
    ],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        ],
)
