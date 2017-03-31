"""Here you can control the config parameters to run Kytos controller.

Basically you can use a config file (-c option) and use arguments on command
line. If you specify a config file, then and option configured inside this file
will be overridden by the option on command line.
"""

import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from configparser import ConfigParser

from kytos.core._metadata import __version__

if 'VIRTUAL_ENV' in os.environ:
    BASE_ENV = os.environ['VIRTUAL_ENV']
else:
    BASE_ENV = '/'


class KytosConfig():
    """KytosConfig class handle settings of Kytos."""

    def __init__(self):
        """Constructor of KytosConfig.

        The contructor set defaults parameters that can be used by KytosConfig.
        """
        self.options = {}
        conf_parser = ArgumentParser(add_help=False)

        conf_parser.add_argument("-c", "--conf",
                                 help="Specify a config file",
                                 metavar="FILE")

        parser = ArgumentParser(prog='kytosd',
                                parents=[conf_parser],
                                formatter_class=RawDescriptionHelpFormatter,
                                description=__doc__)

        parser.add_argument('-v', '--version',
                            action='version',
                            version="kytosd %s" % __version__)

        parser.add_argument('-D', '--debug',
                            action='store_true',
                            help="Run in debug mode")

        parser.add_argument('-f', '--foreground',
                            action='store_true',
                            help="Run in foreground (ctrl+c to stop)")

        parser.add_argument('-l', '--listen',
                            action='store',
                            help="IP/Interface to be listened")

        parser.add_argument('-n', '--napps',
                            action='store',
                            help="Specify the napps directory")

        parser.add_argument('-P', '--port',
                            action='store',
                            help="Port to be listened")

        parser.add_argument('-p', '--pidfile',
                            action='store',
                            help="Specify the PID file to save.")

        parser.add_argument('-w', '--workdir',
                            action='store',
                            help="Specify the working directory")

        self.conf_parser, self.parser = conf_parser, parser
        self.parse_args()

    def parse_args(self):
        """Get the command line options and update kytos settings.

        When installed via pip, defaults values are:

        defaults = {'pidfile': '/var/run/kytosd.pid',
                    'workdir': '/var/lib/kytos',
                    'napps': '/var/lib/kytos/napps/',
                    'conf': '/etc/kytos/kytos.conf',
                    'logging': '/etc/kytos/logging.ini',
                    'listen': '0.0.0.0',
                    'port': 6633,
                    'foreground': False,
                    'debug': False}
        """
        defaults = {'pidfile': os.path.join(BASE_ENV, 'var/run/kytosd.pid'),
                    'workdir': os.path.join(BASE_ENV, 'var/lib/kytos'),
                    'napps': os.path.join(BASE_ENV, 'var/lib/kytos/napps/'),
                    'installed_napps': os.path.join(BASE_ENV,
                                                    'var/lib/kytos/napps/',
                                                    '.installed'),
                    'conf': os.path.join(BASE_ENV, 'etc/kytos/kytos.conf'),
                    'logging': os.path.join(BASE_ENV, 'etc/kytos/logging.ini'),
                    'listen': '0.0.0.0',
                    'port': 6633,
                    'foreground': False,
                    'debug': False}

        options, argv = self.conf_parser.parse_known_args()

        config = ConfigParser()
        result = config.read([options.conf or defaults.get('conf')])

        if result:
            defaults.update(dict(config.items("daemon")))
        else:
            print('There is no config file.')
            exit(-1)

        self.parser.set_defaults(**defaults)

        if 'test' in argv:
            argv.pop(argv.index('test'))

        self.options['daemon'] = self.parser.parse_args(argv)
