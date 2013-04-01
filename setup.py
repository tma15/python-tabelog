#!/usr/bin/python
#-*- coding:utf8 -*-
from setuptools import setup

setup(name='python-tabelog',
      version='1.0',
      description = 'Python wrapper for Tabelog API',
      author='Takuya Makino',
      author_email = 'takuyamakino15@gmail.com',
      url = 'https://github.com/tma15/python-tabelog',
      packages = ['tabelog'],
      install_requires=['BeautifulSoup==3.2.1'],
    )
