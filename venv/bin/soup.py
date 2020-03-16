#!/home/alpesh/PycharmProjects/btp1/venv/bin/python
import argparse
import argcomplete
import os
import getpass

import pysoup


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quiet', help='no output to screen', action='store_true')

    commands = parser.add_subparsers(dest='command')

    cmd_install = commands.add_parser('install', help='install dependencies for a python project')
    cmd_install.add_argument('-g', '--global-installation', help='install dependencies as global', action='store_true')
    cmd_install.add_argument('-r', '--require-custom-file', help='use custom yaml file', default='soup.yaml')

    cmd_init = commands.add_parser('init', help='create a new yaml file for your project')
    cmd_init.add_argument('-n', '--name', help='project name', required=True)
    cmd_init.add_argument('-v', '--version', help='project version', required=False, default='0.0.1')
    cmd_init.add_argument('-a', '--author', help='project author', required=False, default=getpass.getuser())
    cmd_init.add_argument('-r', '--repository', help='project repository', required=False, default='')

    cmd_add = commands.add_parser('add', help='add a dependency to the yaml file')
    cmd_add.add_argument('name', help='name of the dependency', nargs='?')
    cmd_add.add_argument('version', help='version of the dependency', nargs='?')
    cmd_add.add_argument('-r', '--from-requirements', help='import dependencies from pip requirements.txt file', action='store_true')

    cmd_set = commands.add_parser('set', help='set a property in the yaml file')
    cmd_set.add_argument('-n', '--name', help='project name', required=False, default='')
    cmd_set.add_argument('-v', '--version', help='project version', required=False, default='')
    cmd_set.add_argument('-a', '--author', help='project author', required=False, default='')
    cmd_set.add_argument('-r', '--repository', help='project repository', required=False, default='')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.command == 'install':
        cwd = os.getcwd()
        target_file = args.require_custom_file
        is_global = args.global_installation
        is_quiet = args.quiet
        pysoup.PySoup.start_with_args('install', cwd, target_file, is_global, is_quiet)

    if args.command == 'init' or args.command == 'set':
        cwd = os.getcwd()
        target_file = 'soup.yaml'
        is_global = False
        is_quiet = args.quiet
        custom_configuration = {'name': args.name,
                                'version': args.version,
                                'author': args.author,
                                'repository': args.repository}

        if custom_configuration.values() == ['' for i in xrange(len(custom_configuration))]:
            print 'at least one argument is required.\nsee: soup {0} -h'.format(args.command)
        else:
            pysoup.PySoup.start_with_args(args.command,
                                          cwd,
                                          target_file,
                                          is_global,
                                          is_quiet,
                                          custom_configuration=custom_configuration)

    if args.command == 'add':
        cwd = os.getcwd()
        target_file = 'soup.yaml'
        is_global = False
        is_quiet = args.quiet
        if not args.name and not args.from_requirements:
            print 'at least one argument is required.\nsee: soup {0} -h'.format(args.command)
        elif args.name and args.from_requirements:
            print 'cannot do both at the same time.\nsee: soup {0} -h'.format(args.command)
        else:
            version = args.version or '*'
            custom_configuration = {'dependencies': {args.name: version}}
            from_requirements = args.from_requirements
            pysoup.PySoup.start_with_args('add',
                                          cwd,
                                          target_file,
                                          is_global,
                                          is_quiet,
                                          custom_configuration=custom_configuration,
                                          from_requirements=from_requirements)

if __name__ == '__main__':
    main()
