import os
import sys
import inspect
import setuptools
from setuptools import setup, find_packages


package_dir = '.' # the directory that would get added to the path, expressed relative to the location of this setup.py file



try: __file__
except:
	try: frame = inspect.currentframe(); __file__ = inspect.getfile( frame )
	finally: del frame  # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
HERE = os.path.realpath( os.path.dirname( __file__ ) )


setup_args = dict(name='PigeonPy',
package_dir={ '' : package_dir },
		version='1.0.0', # @VERSION_INFO@
		packages=find_packages(),
		include_package_data=True,
		description='A simple email notification package with GUI setup for credentials.',
		long_description=open('README.md', encoding='utf-8').read(),
		long_description_content_type='text/markdown',
		url='https://github.com/ludvikalkhoury/PigeonPy.git',
		author='Ludvik Alkhoury',
		author_email='Ludvik.alkhoury@gmail.com',
		#packages=['PigeonPy'],
		classifiers=[
			'Programming Language :: Python :: 3',
			'Operating System :: OS Independent',
		],
		python_requires='>=3.6',
		entry_points={
			'console_scripts': [
				'email-notifier-setup=PigeonPy.gui_setup:launch_setup'
			]},
		install_requires=[])

      
if __name__ == '__main__' and getattr( sys, 'argv', [] )[ 1: ]:
	setuptools.setup( **setup_args )
else:
	sys.stderr.write( """
The PigeonPy setup.py file should not be run or imported directly.
Instead, it is used as follows:

    python -m pip install -e  "%s"

""" % HERE )






