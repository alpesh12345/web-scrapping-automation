import os.path

from twisted.internet import defer

import pysoup.utils


class Virtualenv(object):

    def __init__(self, display_pip, path):
        self._display_pipe = display_pip
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def venv_path(self):
        return os.path.join(self._path, 'venv')

    @property
    def source_path(self):
        return os.path.join(self.venv_path, 'bin/activate')

    @defer.inlineCallbacks
    def create(self):
        self._display_pipe.log('Ensuring virtualenv environment at {0}'.format(self._path))

        code = yield pysoup.utils.execute_shell_command('mkdir -p {0} && virtualenv --no-site-packages -q {0}'.format(self.venv_path))
        if code != 0:
            self._display_pipe.error('Failed to setup virtualenv at target! ({0})'.format(self._path))
            raise Exception('Could not create virtualenv')

        self._display_pipe.notify('Virtualenv is ready')

    @defer.inlineCallbacks
    def execute_in_venv(self, command):
        code = yield pysoup.utils.execute_shell_command('source {0} && {1}'.format(self.source_path, command))
        defer.returnValue(code)
