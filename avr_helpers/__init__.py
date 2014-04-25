"""
Copyright 2011 Ryan Fobel

This file is part of dmf_control_board.

dmf_control_board is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

dmf_control_board is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with dmf_control_board.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from subprocess import Popen, PIPE, CalledProcessError
import logging

from path_helpers import path
from serial_device import SerialDevice, ConnectionError


logger = logging.getLogger()


class FirmwareError(Exception):
    pass


class AvrDude(SerialDevice):
    def __init__(self, port=None):
        p = path(os.path.abspath(os.path.dirname(__file__)))
        if os.name == 'nt':
            self.avrdude = (p / path('avrdude.exe')).abspath()
        else:
            self.avrdude = (p / path('avrdude')).abspath()
        logger.info("avrdude path=%s" % self.avrdude)
        if not self.avrdude.exists():
            raise FirmwareError('avrdude not installed')
        self.avrconf = (p / path('avrdude.conf')).abspath()
        if port:
            self.port = port
            logger.info('avrdude set to connect on port: %s' % self.port)
        else:
            self.port = self.get_port(115200)
            logger.info('avrdude successfully connected on port: %s' % self.port)

    def _run_command(self, flags):
        config = dict(avrdude=self.avrdude, avrconf=self.avrconf)

        cmd = ['%(avrdude)s'] + flags
        cmd = [v % config for v in cmd]

        logger.info(' '.join(cmd))
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode:
            raise ConnectionError(stderr)
        return stdout, stderr

    def flash(self, hex_path):
        hex_path = path(hex_path)
        flags = ['-c', 'stk500v2', '-b', '115200', '-p', 'atmega2560',
                    '-P', '%s' % self.port,
                    '-U', 'flash:w:%s' % hex_path.name,
                    '-C', '%(avrconf)s']


        try:
            cwd = os.getcwd()
            os.chdir(hex_path.parent)
            stdout, stderr = self._run_command(flags)
        finally:
            os.chdir(cwd)
        return stdout, stderr

    def test_connection(self, port, baud_rate):
        flags = ['-c', 'stk500v2', '-b', baud_rate, '-p', 'atmega2560',
                    '-P', port,
                    '-C', '%(avrconf)s', '-n']
        try:
            self._run_command(flags)
        except (ConnectionError, CalledProcessError):
            return False
        return True
