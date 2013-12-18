#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

#long_description = open('./README.rest', 'r').read()
long_description = 'A schema free database by useing python dict'
description = 'A scheem free database by useing python dict'

setup(name='DictDB',
      version='0.0.0',
      description=description,
      long_description=long_description,
      author='Toomore Chiang',
      author_email='toomore0929@gmail.com',
      url='https://github.com/toomore/dictDB',
      py_modules=['dictdb'],
      #packages=['dictdb'],
      #include_package_data=True,
      license='MIT',
      keywords="dict schema-free database",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Chinese (Traditional)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Database :: Front-Ends',
          ],
     )
