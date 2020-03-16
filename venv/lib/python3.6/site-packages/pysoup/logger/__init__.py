import os.path

import pysoup.utils.assets

class Logger(object):

    def __init__(self, cwd):
        self._log = ''
        self._cwd = cwd

    def log(self, text):
        self._log += '{0}\n'.format(text)

    def log_dependency_results(self, failed_dependencies):
        for dependency in failed_dependencies:
            self.log('could not install {0}'.format(dependency))

    def dump_to_file(self, filename='soup.log'):
        if self._log != '':
            with open(os.path.join(self._cwd, filename), 'wb') as f:
                f.write(pysoup.utils.assets.LOGO)
                f.write('\n{0}'.format(self._log))
