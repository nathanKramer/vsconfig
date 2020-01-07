import sys
import cli
from vsconfig import diff, help, install, reset


def run_cmd(cmd, flags):
    if cmd == None:
        help()
        return
    named_flags = cli.parse_flags(flags)
    extension_file = named_flags.get('file', 'extensions')
    if cmd == 'diff':
        diff(extension_file)
    elif cmd == 'help':
        help_topic = None
        if len(flags) > 0:
            help_topic = flags[0]
        help(help_topic)
    elif cmd == 'install':
        install(extension_file)
    elif cmd == 'reset':
        reset(extension_file)
    else:
        print(f'Unknown command: {cmd}')
        help()


def main():
    cmd = None
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    flags = sys.argv[2:]
    run_cmd(cmd, flags)


if __name__ == "__main__":
    main()
