#!/usr/bin/env python3
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
    print(f'{bcolors.OKBLUE}[VSConfig]: Uninstalling {len(extensions)} extensions...{bcolors.ENDC}')
    [ code_cmd('uninstall-extension', extension) for extension in extensions ] 


def install_extensions(extensions):
    print(f'{bcolors.OKBLUE}[VSConfig]: Installing {len(extensions)} extensions...{bcolors.ENDC}')
    [ code_cmd('install-extension', extension) for extension in extensions ]



# Extensions



def extensions_set(extensions_str):
    return set(extensions_str.split('\n'))


def declared_extensions(extension_file):
    with open(extension_file, 'r') as extensions_file:
        extensions = set()
        [ extensions.add(line.strip()) for line in extensions_file.readlines() ]
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



# API



def help(cmd=None):
    if cmd:
        print("Command specific help")
        return

    with open(f'{filepath}/help/usage', 'r') as help_text:
        print(''.join(help_text.readlines()))

def diff(extension_file):
    missing, extra = diff_extensions(extension_file)
    work = len(missing) + len(extra)
    if work == 0:
        print(f'{bcolors.OKGREEN}Up-to-date{bcolors.ENDC}')
        return

    if len(missing) > 0:
        missingL = list(missing)
        missingL.sort()
        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Not Currently Installed:{bcolors.ENDC}\n' +
            '\n'.join(map(lambda str: f'{bcolors.OKBLUE}+{bcolors.ENDC} {str}', missingL)))
    if len(extra) > 0:
        extraL = list(extra)
        extraL.sort()
        print(f'{bcolors.WARNING}Untracked extensions:{bcolors.ENDC}\n' +
            '\n'.join(map(lambda str: f'{bcolors.WARNING}-{bcolors.ENDC} {str}', extraL)))


def install(extension_file):
    missing, _ = diff_extensions(extension_file)
    if len(missing) > 0: install_extensions(missing)

def reset(extension_file):
    missing, extra = diff_extensions(extension_file)
    if len(extra) > 0: uninstall_extensions(extra)
    if len(missing) > 0: install_extensions(missing)
