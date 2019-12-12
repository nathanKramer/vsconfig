#!/usr/bin/env python3
import subprocess
import sys



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


def uninstall_extensions(extensions):
    for extension in extensions:
        print(
            subprocess.check_output(
                'code --uninstall-extension ' + extension, shell=True).decode('utf-8')
        )


def install_extensions(extensions):
    for extension in extensions:
        print(
            subprocess.check_output(
                'code --install-extension ' + extension, shell=True).decode('utf-8')
        )

# Extensions


def extensions_set(extensions_str):
    return set(extensions_str.split('\n'))


def declared_extensions():
    with open('extensions', 'r') as extensions_file:
        extensions = set()
        for line in extensions_file.readlines():
            extensions.add(line.strip())
        return extensions


def installed_extensions():
    result = subprocess.check_output('code --list-extensions', shell=True)
    return extensions_set(result.decode('utf-8').strip())


def main():
    installed = installed_extensions()
    declared = declared_extensions()

    missing = declared - installed
    extra = installed - declared

    use_case = sys.argv[1]
    if not use_case:
        use_case = 'install'

    if use_case == 'diff':
        work = len(missing) + len(extra)
        if work == 0:
            print(f'{bcolors.OKGREEN}Up-to-date{bcolors.ENDC}')
            return

        if len(missing) > 0:
            print(f'{bcolors.OKBLUE}{bcolors.BOLD}Not Currently Installed:{bcolors.ENDC}\n' +
                '\n'.join(map(lambda str: f'- {str}', missing))
                )
        if len(extra) > 0:
            print(f'{bcolors.WARNING}Untracked extensions:{bcolors.ENDC}\n' +
                '\n'.join(map(lambda str: f'- {str}', extra)))

    if use_case == 'force':
        if len(extra) > 0:
            uninstall_extensions(extra)

    if use_case == 'install' or use_case == 'force':
        if len(missing) > 0:
            install_extensions(missing)


if __name__ == "__main__":
    main()

# Preferences
