class Display(object):

    def __init__(self):
        pass

    def create_pipe(self):
        raise NotImplementedError()

    def update(self, key, message, type):
        raise NotImplementedError()


class DisplayPipe(object):

    def __init__(self, display, key):
        self._display = display
        self._key = key

    def log(self, message):
        self._update_display(message, 'log')

    def success(self, message):
        self._update_display(message, 'success')

    def error(self, message):
        self._update_display(message, 'error')

    def notify(self, message):
        self._update_display(message, 'notify')

    def _update_display(self, message, type):
        self._display.update(self._key, message, type)
