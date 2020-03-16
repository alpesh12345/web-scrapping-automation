import os.path

from twisted.internet import defer, reactor

import pysoup.logger
import pysoup.display
import pysoup.parser
import pysoup.pip
import pysoup.utils
import pysoup.venv


class PySoup(object):

    def __init__(self, display, path, is_global):
        self._path = path
        self._is_global = is_global

        self._logger = pysoup.logger.Logger(path)

        self._parser = pysoup.parser.Parser()

        self._display = display
        self._display_pipes = {}
        self._add_display_pipe('sys')

        self._venv = None
        self._pip = None

    @defer.inlineCallbacks
    def install_from_file(self, target_config_file):
        self._display_pipes['sys'].log('Loading configuration file...')
        try:
            configuration = self._parser.parse_file(target_config_file)
        except:
            self._display_pipes['sys'].error('Could not load target file!')
            raise PysoupExecutionError()

        self._venv = self._create_venv()
        if not self._is_global:
            self._display_pipes['sys'].log('Setting up virtualenv...')
            try:
                yield self._venv.create()
            except:
                self._display_pipes['sys'].error('Could not setup virtualenv!')
                raise PysoupExecutionError()

        failed_dependencies = None
        if configuration.has_key('dependencies'):
            self._pip = self._create_pip()
            self._display_pipes['sys'].log('Installing pip dependencies...')
            _, failed_dependencies = yield self._pip.install_dependencies(configuration['dependencies'])
        else:
            self._display_pipes['sys'].log('No dependencies to install, skipping...')

        if not failed_dependencies:
            self._display_pipes['sys'].success('Done!')
        else:
            self._display_pipes['sys'].error('Done, but some dependencies were not installed. See soup.log')
            self._logger.log_dependency_results(failed_dependencies)

        self._logger.dump_to_file()
        yield 'completed'

    @defer.inlineCallbacks
    def init_new_project(self, configuration, target_config_file):
        if os.path.exists(target_config_file):
            self._display_pipes['sys'].notify('target file already exists, aborting...')
        else:
            yield self._update_project_attributes(configuration, target_config_file)

        yield 'completed'

    @defer.inlineCallbacks
    def set_project_attributes(self, configuration, target_config_file):
        if not os.path.exists(target_config_file):
            self._display_pipes['sys'].notify('soup configuration does not exists, aborting...')
        else:
            yield self._update_project_attributes(configuration, target_config_file)

        yield 'completed'

    @defer.inlineCallbacks
    def add_dependencies_from_pip_requirements(self, pip_requirements_path, target_config_file):
        configuration = None

        try:
            configuration = self._parser.parse_pip_requirements(pip_requirements_path)
        except:
            self._display_pipes['sys'].notify('could not parse requirements file, aborting...')
            defer.returnValue(None)

        yield self.add_dependencies(configuration, target_config_file)

        yield 'completed'

    @defer.inlineCallbacks
    def add_dependencies(self, configuration, target_config_file):
        try:
            target_config = self._parser.parse_file(target_config_file)

            try:
                target_dependencies = target_config['dependencies']
            except:
                target_dependencies = {}

            for dependency, version in configuration['dependencies'].iteritems():
                target_dependencies[dependency] = version

            target_config['dependencies'] = target_dependencies

            self._parser.dump_to_file(target_config, target_config_file)

            self._display_pipes['sys'].success('dependency added successfully!')
        except:
            self._display_pipes['sys'].notify('soup configuration does not exists, aborting...')

        yield 'completed'

    @defer.inlineCallbacks
    def _update_project_attributes(self, configuration, target_config_file):
        new_config = {key: value for key, value in configuration.iteritems() if value}

        try:
            old_config = self._parser.parse_file(target_config_file)

            for key, value in old_config.iteritems():
                if not new_config.has_key(key):
                    new_config[key] = value
        except:
            pass

        self._parser.dump_to_file(new_config, target_config_file)
        self._display_pipes['sys'].success('soup configuration was updated successfuly!')

        yield 'completed'

    def _add_display_pipe(self, pipe_name):
        self._display_pipes[pipe_name] = self._display.create_pipe()
        return self._display_pipes[pipe_name]

    def _create_venv(self):
        if not self._is_global:
            return pysoup.venv.Virtualenv(self._add_display_pipe('venv'), self._path)
        else:
            return None

    def _create_pip(self):
        return pysoup.pip.Pip(self._add_display_pipe('pip'), venv=self._venv)

    @staticmethod
    def start_with_args(command, cwd, target_config_file, is_global=False, is_silent=False, custom_configuration=None, from_requirements=False):
        if is_silent:
            display = pysoup.display.DisplayAdapter.create_silent_display()
        else:
            display = pysoup.display.DisplayAdapter.create_interactive_display()

        soup = PySoup(display, cwd, is_global)

        exec_command = None

        if command == 'install':
            file_path = os.path.join(cwd, target_config_file)
            exec_command = soup.install_from_file(file_path)

        elif command == 'init':
            file_path = os.path.join(cwd, target_config_file)
            exec_command = soup.init_new_project(custom_configuration, file_path)

        elif command == 'set':
            file_path = os.path.join(cwd, target_config_file)
            exec_command = soup.set_project_attributes(custom_configuration, file_path)

        elif command == 'add':
            file_path = os.path.join(cwd, target_config_file)
            if from_requirements:
                pip_requirements_path = os.path.join(cwd, 'requirements.txt')
                exec_command = soup.add_dependencies_from_pip_requirements(pip_requirements_path, file_path)
            else:
                exec_command = soup.add_dependencies(custom_configuration, file_path)


        exec_command.addCallbacks(PySoup._on_soup_callback, PySoup._on_soup_errback)
        reactor.run()

    @staticmethod
    def _on_soup_callback(result):
        PySoup._teardown(0)

    @staticmethod
    def _on_soup_errback(error):
        PySoup._teardown(1)

    @staticmethod
    def _teardown(exit_code):
        reactor.callFromThread(reactor.stop)


class PysoupExecutionError(Exception):
    pass
