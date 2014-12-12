import os
import inspect
from datetime import datetime
from argparse import ArgumentParser

import ed25519

from dhall.log import logger

class CommandlineArgumentError(Exception):
    pass

def cmd_sign(argv):
    """
    Sign file
    """
    description = inspect.getdoc(cmd_sign)
    parser = ArgumentParser(description=description)
    parser.add_argument("-k","--key", action="store", dest="key",
        default='dhall_key', help="signing key")
    parser.add_argument("files", action="store", nargs="+",
        default=None, help="Files to sign")

    args = parser.parse_args(argv)

    if not os.path.exists(args.key):
        import dhall.util
        sign_key, verify_key = dhall.util.generate_keys(args.key)
    else:
        try:
            sign_key = ed25519.SigningKey(open(args.key,"rb").read())
            verify_key = sign_key.get_verifying_key()
        except Exception,e:
            logger.error("Error loading signing key %s" % args.key)
            raise e

    for f in args.files:
        logger.info("Signing file %s" % f)
        try:
            sig = sign_key.sign(open(f, 'rb').read(), encoding='base64')
            open("%s.sig" % f, 'wb').write(sig)
            logger.info("Signature: %s" % sig)
        except IOError, e:
            logger.error("Can't open file %s: %s" % (f,e))
            continue


def cmd_verify(argv):
    """
    Verify digital signature
    """
    description = inspect.getdoc(cmd_verify)
    parser = ArgumentParser(description=description)
    parser.add_argument("-s","--sig", action="store", dest="sig",
        default=None, help="signature file")
    parser.add_argument("-k","--key", action="store", dest="key",
        default="dhall_key.pub", help="verifying key")
    parser.add_argument("files", action="store", nargs="+",
        default=None, help="Files to verify")
    args = parser.parse_args(argv)

    if not args.key:
        parser.error("A verifying key is needed")

    try:
        vkey = ed25519.VerifyingKey(open(args.key, 'rb').read(),
            encoding="hex")
    except Exception,e:
        logger.error("Error loading verification key %s" % args.key)
        raise

    for f in args.files:
        logger.info("Verifying file %s" % f)
        if not args.sig: args.sig = "%s.sig" % f
        try:
            sig = open(args.sig, 'r').read()
            vkey.verify(sig, open(f, 'rb').read(), encoding='base64')
            logger.info("Signature is good")
        except IOError, e:
            logger.error("Couldn't open signature file %s.sig: %s" %(f,e))
            continue
        except ed25519.BadSignatureError:
            logger.error("Signature is bad")


def cmd_generate(argv):
    """
    Generate signing and verifying keys
    """
    description = inspect.getdoc(cmd_generate)
    parser = ArgumentParser(description=description)
    parser.add_argument("-o","--output", action="store", dest="output",
        default="dhall_key", help="outpuf filename")
    args = parser.parse_args(argv)

    import dhall.util
    dhall.util.generate_keys(key=args.output)


def cmd_help(argv):
    """
    List available commands
    """
    description = inspect.getdoc(cmd_help)
    parser = ArgumentParser(description=description)
    parser.add_argument("command", nargs="?", action="store",
        default=None, help="Command to print help for")

    args = parser.parse_args(argv)

    import dhall.util
    cmds = dhall.util.discover_commands()
    if args.command:
        try:
            cmds[args.command]({}, ['--help'])
        except KeyError:
            raise Exception("Command not found")

    logger.info("Available commands:")

    for k in sorted(cmds.keys()):
        logger.info("  {:16}\t{}".format(k, inspect.getdoc(cmds[k])))
