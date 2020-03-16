from pysoup.display._display import Display, DisplayPipe


class SilentDisplay(Display):

    def __init__(self):
        super(SilentDisplay, self).__init__()

    def create_pipe(self):
        return DisplayPipe(self, '')

    def update(self, key, message, type):
        pass
