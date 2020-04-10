#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Created by Mika Bostrom, released into the public domain as far as legally possible.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
from setuptools import setup, find_packages


setup(
    name='fpdb',
    description='Free Poker Database',
    version='0.30',
    author='FPDB team',
    author_email='fpdb-main@lists.sourceforge.net',
    packages=find_packages(),
    include_package_data=True
)
