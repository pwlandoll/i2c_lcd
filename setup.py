# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
    "smbus-cffi"
]

test_requirements = [
    # TODO: put package test requirements here
    "nose",
    "smbus-cffi"
]

setup(
    name='i2c_lcd',
    version='0.1.0',
    description="I2C LCD interface in Python made for RPi.",
    long_description=readme + '\n\n' + history,
    author="Peter Landoll",
    author_email='pwlandoll@gmail.com',
    url='https://github.com/pwlandoll/i2c_lcd',
    packages=[
        'i2c_lcd',
    ],
    package_dir={'i2c_lcd':
                 'i2c_lcd'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='i2c_lcd',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
