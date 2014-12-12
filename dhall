#!/usr/bin/env python

import os, sys, imp, string, getopt
from argparse import ArgumentParser
import pdb
import os.path

__selfpath__ = os.path.abspath(os.path.dirname(__file__))

sys.path.append(__selfpath__ + "/modules")

import dhall.util
from dhall.log import logger
from dhall.log import set_log_level, logger
from dhall.version import __version__, __maintainer__

# This block ensures that ^C interrupts are handled quietly.
try:
    import signal

    def exithandler(signum,frame):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        sys.exit(1)

    signal.signal(signal.SIGINT, exithandler)
    signal.signal(signal.SIGTERM, exithandler)
    if hasattr(signal, 'SIGPIPE'):
                signal.signal(signal.SIGPIPE, signal.SIG_DFL)

except KeyboardInterrupt:
        sys.exit(1)

def main(argv):

    description = ""

    parser = ArgumentParser(
        version=__version__, description=description
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug",
        default=False, help=("enable debug messages")
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", dest="quiet",
        default=False, help="don't print status messages to stdout"
    )
    parser.add_argument(
        "--traceback", action="store_true", dest="trace", default=False,
        help="print full traceback on exceptions"
        )
    parser.add_argument(
        "--disable-colors", action="store_true", dest="color_disable",
        default=(os.name == 'nt' or not sys.stdout.isatty()),
        help="disable colors in the output of commands"
    )
    parser.add_argument("command", nargs='?',
        default="help", help="Command to run [Available commands: help, "\
                "sign, verify, generate]")
    args, remaining_argv = parser.parse_known_args()

    #utils.DISABLE_COLORS = options.color_disable

    # set log level
    if args.quiet:
        set_log_level('WARNING')
    elif args.debug:
        set_log_level('DEBUG')

    cmd = args.command

    try:
        dhall.util.exec_command(cmd, remaining_argv)
    except dhall.util.UnknownCommandError:
        logger.error("dhall: Command %s not found" % cmd)
    except SystemExit:
        sys.exit()
    except:
        import traceback
        if args.trace:
            traceback.print_exc()
        else:
            formatted_lines = traceback.format_exc().splitlines()
            logger.error(formatted_lines[-1])
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
