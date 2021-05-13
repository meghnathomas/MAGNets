#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'cycler==0.10.0',
    'decorator==4.4.2',
    'kiwisolver==1.1.0',
    'matplotlib==3.0.3',
    'networkx==2.4',
    'numpy>=1.19.0rc1',
    'pandas==1.1.5',
    'Pillow==8.2.0',
    'pyparsing==2.4.7',
    'python-dateutil==2.8.1',
    'pytz==2021.1',
    'scipy==1.5.4',
    'six==1.15.0',
    'wntr>=0.3.0'
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Meghna Sarah Thomas",
    author_email='meghnathomas@utexas.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A Python package to aggregate and reduce water distribution network models",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='magnets',
    name='magnets',
    packages=find_packages(include=['magnets', 'magnets.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/meghnathomas/magnets',
    version='0.1.0',
    zip_safe=False,
)
