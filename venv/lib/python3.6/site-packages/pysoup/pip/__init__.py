from twisted.internet import defer

import pysoup.utils


class Pip(object):

    def __init__(self, display_pipe, venv=None):
        self._display_pipe = display_pipe
        self._venv = venv

    @defer.inlineCallbacks
    def install_dependencies(self, dependency_map):
        failed_installations = []
        successful_installations = []
        dependency_count = len(dependency_map)
        current_dependency = 0

        for dependency, version in dependency_map.iteritems():
            current_dependency += 1
            self._display_pipe.log('installing {0} ({1}/{2})'.format(dependency, current_dependency, dependency_count))

            try:
                yield self._install_dependency(dependency, version)
                successful_installations.append(dependency)
            except:
                failed_installations.append(dependency)

        if failed_installations:
            self._display_pipe.error('failed to install {0} dependencies.'.format(len(failed_installations)))
        else:
            self._display_pipe.success('all dependencies installed successfully!')

        defer.returnValue((successful_installations, failed_installations))

    @defer.inlineCallbacks
    def _install_dependency(self, dependency, version=''):
        command = 'pip install "{0}"'.format(self._get_pip_complient_string(dependency, version))

        if self._venv:
            success = yield self._venv.execute_in_venv(command)
        else:
            success = yield pysoup.utils.execute_shell_command(command)

        if success != 0:
            raise Exception('could not install dependency')

    def _get_pip_complient_string(self, dependency, version=''):
        complient_dependency = dependency
        complient_version = pysoup.utils.version_notation_soup_to_pip(version)
        return '{0}{1}'.format(complient_dependency, complient_version)
