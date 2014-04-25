import sys
from pprint import pprint

from paver.easy import task, needs, path
from paver.setuputils import setup, find_package_data

import version
# Add package directory to Python path. This enables the use of `avr_helpers`
# functions for discovering, e.g., the path to the [AVR][1] tools.
#
# [1]: http://en.wikipedia.org/wiki/Atmel_AVR
sys.path.append(path('.').abspath())
import avr_helpers

avr_helpers_files = find_package_data(package='avr_helpers',
                                      where='avr_helpers',
                                      only_in_packages=False)
pprint(avr_helpers_files)

setup(name='avr_helpers',
      version=version.getVersion(),
      description='Minimal tool-set for flashing bit-streams to AVR '
      'micro-controllers.',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='http://github.com/wheeler-microfluidics/avr_helpers.git',
      license='GPLv2',
      packages=['avr_helpers'],
      package_data=avr_helpers_files,
      install_requires=['path_helpers', 'serial_device'])


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
