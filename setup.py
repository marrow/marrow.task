#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import sys
import codecs


# This is an extreme test for use of __qualname__ and im_class.

class Mine(object):
	def canary(self):
		pass

if not hasattr(Mine.canary, 'im_class') and not hasattr(Mine.canary, '__qualname__'):
	os.environ['CANARY'] = "DEAD"
	print("*" * 79, file=sys.stderr)
	print(" WARNING: You are executing marrow.tasks under a Python version that supports", file=sys.stderr)
	print(" neither im_class nor __qualname__ on class methods.  Attempts to use class", file=sys.stderr)
	print(" methods as execution targets WILL FAIL GLORIOUSLY.", file=sys.stderr)
	print(" See: https://github.com/marrow/marrow.task/#21-requirements")
	print("*" * 79, file=sys.stderr)


try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

from setuptools.command.test import test as TestCommand


if sys.version_info < (2, 6):
	raise SystemExit("Python 2.6 or later is required.")
elif sys.version_info > (3, 0) and sys.version_info < (3, 2):
	raise SystemExit("Python 3.2 or later is required.")

exec(open(os.path.join("marrow", "task", "release.py")).read())


class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		
		self.test_args = []
		self.test_suite = True
	
	def run_tests(self):
		import pytest
		sys.exit(pytest.main(self.test_args))


here = os.path.abspath(os.path.dirname(__file__))

tests_require = ['pytest', 'pytest-cov']

setup(
	name = "marrow.task",
	version = version,
	
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	
	author = author.name,
	author_email = author.email,
	
	license = 'MIT',
	keywords = '',
	classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 2.6",
			"Programming Language :: Python :: 2.7",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.2",
			"Programming Language :: Python :: 3.3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules"
		],
	
	packages = find_packages(exclude=['test', 'script', 'example']),
	include_package_data = True,
	namespace_packages = ['marrow'],
	
	install_requires = ['mongoengine', 'pytz'],
	
	extras_require = dict(
			development = tests_require,
		),
	
	tests_require = tests_require,
	
	zip_safe = False,
	cmdclass = dict(
			test = PyTest,
		)
)
