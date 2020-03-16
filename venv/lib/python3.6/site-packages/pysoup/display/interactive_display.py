import blessings
import sys
import os.path

from pysoup.display._display import Display, DisplayPipe

import pysoup.utils
import pysoup.utils.assets

class InteractiveDisplay(Display):

    graphical_assets_directory = os.path.join(os.path.dirname(__file__), '../../assets')

    def __init__(self):
        super(InteractiveDisplay, self).__init__()
        self._blessings = blessings.Terminal()
        self._lines = []

        self._clear_screen()
        self._print_logo()

    def create_pipe(self):
        key = len(self._lines)
        self._lines.append('')
        print ''
        self._refresh()
        return DisplayPipe(self, key)

    def update(self, key, message, type):
        self._lines[key] = self._format_message(message, type)
        self._refresh()

    def _refresh(self):
        output = self._clean()

        for line in self._lines:
            output += line + '\n'

        print output,

    def _format_message(self, message, type):
        max_line_length = sys.maxint
        message = '{0}'.format(str(message)[:max_line_length])
        if type == 'success':
            return self._blessings.green(message)
        elif type == 'error':
            return self._blessings.red(message)
        elif type == 'notify':
            return self._blessings.bright_yellow(message)
        else:
            return self._blessings.white(message)

    def _clear_screen(self):
        print self._blessings.clear

    def _clean(self):
        return (self._blessings.move_up * len(self._lines)) + self._blessings.clear_eos

    def _print_logo(self):
        print pysoup.utils.assets.LOGO
