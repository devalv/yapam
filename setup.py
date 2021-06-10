# -*- coding: utf-8 -*-
"""Python package config."""
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='yapam',
    version='0.1.4',
    author='Devyatkin Aleksei',
    author_email='yapam@devyatkin.dev',
    description='Yet another ammo maker',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devalv/yapam',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=['dav-utils==0.2.*']
)
