import pysoup.display.interactive_display
import pysoup.display.silent_display


class DisplayAdapter(object):

    @staticmethod
    def create_interactive_display():
        return pysoup.display.interactive_display.InteractiveDisplay()

    @staticmethod
    def create_silent_display():
        return pysoup.display.silent_display.SilentDisplay()
