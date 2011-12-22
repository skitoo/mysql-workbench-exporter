#!/usr/bin/env python

from setuptools import setup, find_packages
import os, mworkbenchexporter


setup(
      author = 'Alexis Couronne',
      author_email = 'alexis.couronne@scopart.fr',
      name = 'mysql-workbench-exporter',
      version = mworkbenchexporter.__version__,
      description = 'MySQLWorkbenchExporter is a tool that allows you to export MySQLWorkbench schemas to engines like Doctrine2.',
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      keywords = 'mysqlworkbench doctrine',
      url = 'https://github.com/skitoo/mysql-workbench-exporter',
      license = 'New BSD License',
      platforms = ['OS Independent'],
      scripts=['bin/mwbexporter'],
      #classifiers = CLASSIFIERS,
      packages = find_packages()
)


