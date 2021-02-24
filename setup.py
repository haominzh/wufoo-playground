#!python

from setuptools import setup, find_packages

setup(
    name="wufoo-playground",
    version="0.0.1",
    author="Haomin Zhang",
    url="https://github.com/haominzh/wufoo-playground",
    description='Wufoo REST API playground',
    long_description=open('README.md').read(),
    keywords='python',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        ],
    packages=find_packages(),
    include_package_data=True,
    )
