#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import subprocess
import os

filepath = os.path.dirname(os.path.abspath(__file__))


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Extension Management


def code_cmd(cmd_name, arg):
    print(
        subprocess.check_output(
            f'code --{cmd_name} {arg}', shell=True).decode('utf-8')
    )


def uninstall_extensions(extensions):
    print(
        f'{bcolors.OKBLUE}[VSConfig]: Uninstalling {len(extensions)} extensions...{bcolors.ENDC}')
    [code_cmd('uninstall-extension', extension) for extension in extensions]


def install_extensions(extensions):
    print(
        f'{bcolors.OKBLUE}[VSConfig]: Installing {len(extensions)} extensions...{bcolors.ENDC}')
    [code_cmd('install-extension', extension) for extension in extensions]


# Extensions


def extensions_set(extensions_str):
    return set(extensions_str.split('\n'))


def declared_extensions(extension_file):
    with open(extension_file, 'r') as extensions_file:
        extensions = set()
        [extensions.add(line.strip()) for line in extensions_file.readlines()]
        return extensions


def installed_extensions():
    result = subprocess.check_output('code --list-extensions', shell=True)
    return extensions_set(result.decode('utf-8').strip())


def diff_extensions(extension_file):
    installed = installed_extensions()
    declared = declared_extensions(extension_file)

    missing = declared - installed
    extra = installed - declared
    return [missing, extra]


# Extension Metadata


def parse_extension_metadata(extension_metadata_f):
    xml = ET.parse(extension_metadata_f)
    # Do way more shit here
    return xml


def index_extension_metadata(installed_extensions, extensions_path):
    # This should load all .vsixmanifests
    # The metadata should be used to make decisions about which extensions should be uninstalled first
    # This helps for extensions packs, where the main extension should be uninstalled rather than any of its children
    # It may also be useful to use the extension dependency information to ensure that extensions with dependencies are uninstalled last
    exts = os.listdir(extensions_path)

    def extension_folder_name(ext): return next(
        filter(lambda extname: extname.startswith(ext.lower()), exts)
    )
    def extension_path(
        ext): return f'{extensions_path}/{extension_folder_name(ext)}/.vsixmanifest'

    def parse_metadata(ext): return (
        parse_extension_metadata(
            extension_path(ext))
    )

    extension_dict = {ext: parse_metadata(ext) for ext in installed_extensions}
    return extension_dict

# API


def help(cmd=None):
    if not cmd:
        help(cmd='usage')
        return

    file_name = f'{filepath}/help/{cmd}'
    if not os.path.exists(file_name) or not os.path.isfile(file_name):
        print(f'Unknown command: {cmd}')
        help(cmd='usage')
        return

    # Cmd specific help text
    with open(file_name, 'r') as help_text:
        print(help_text.read())


def diff(extension_file):
    missing, extra = diff_extensions(extension_file)
    work = len(missing) + len(extra)
    if work == 0:
        print(f'{bcolors.OKGREEN}Up-to-date{bcolors.ENDC}')
        return
    if len(missing) > 0:
        missingL = list(missing)
        missingL.sort()
        print(f'{bcolors.OKBLUE}{bcolors.BOLD}[Missing] In extension file but not installed:{bcolors.ENDC}\n' +
              '\n'.join(map(lambda str: f'{bcolors.OKBLUE}+{bcolors.ENDC} {str}', missingL)))
    if len(extra) > 0:
        extraL = list(extra)
        extraL.sort()
        print(f'{bcolors.WARNING}[New] Installed but not in extension file:{bcolors.ENDC}\n' +
              '\n'.join(map(lambda str: f'{bcolors.WARNING}-{bcolors.ENDC} {str}', extraL)))


def install(extension_file):
    missing, _ = diff_extensions(extension_file)
    if len(missing) > 0:
        install_extensions(missing)


def reset(extension_file):
    missing, extra = diff_extensions(extension_file)
    if len(extra) > 0:
        uninstall_extensions(extra)
    if len(missing) > 0:
        install_extensions(missing)
