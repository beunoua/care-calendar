#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="beunoua",
    author_email='beunoua',
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
    description="Calendar for children custody",
    entry_points={
        'console_scripts': [
            'care_calendar=care_calendar.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='care_calendar',
    name='care_calendar',
    packages=find_packages(include=['care_calendar', 'care_calendar.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/beunoua/care_calendar',
    version='0.1.1',
    zip_safe=False,
)
