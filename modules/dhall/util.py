import os
import re
import tarfile
import urllib2

class UnknownCommandError(Exception):
    pass

class ExtractError(Exception):
    pass

class DownloadError(Exception):
    pass

def generate_keys(key=None):
    import ed25519
    from dhall.log import logger

    sign_key, verify_key = ed25519.create_keypair()
    logger.info("Generating signing key %s" % key)
    logger.debug("Signing key %s" % sign_key.to_ascii(encoding="hex"))
    if key: open(key, "wb").write(sign_key.to_bytes())
    logger.info("Generating verifying key %s.pub" % key)
    logger.debug("Signing key %s" % sign_key.to_ascii(encoding="hex"))
    if key: open("%s.pub" % key, "wb").write(
            verify_key.to_ascii(encoding="hex"))

    return sign_key, verify_key

def discover_commands():
    """
    Inspect commands.py and find all available commands
    """
    import inspect
    from dhall import commands

    command_table = {}
    fns = inspect.getmembers(commands, inspect.isfunction)

    for name, fn in fns:
        if name.startswith("cmd_"):
            command_table.update({
                name.split("cmd_")[1]:fn
            })

    return command_table


def exec_command(command, *args, **kwargs):
    """
    Execute given command
    """
    commands = discover_commands()
    try:
        cmd_fn = commands[command]
    except KeyError:
        raise UnknownCommandError
    cmd_fn(*args,**kwargs)
