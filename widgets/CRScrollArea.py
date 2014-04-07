import urwid


class CRScrollArea(urwid.BoxWidget):

    def __init__(self, content):
        self._content = content

    def render(self, size, focus=False):
        return self._content.render(size, focus)

    def keypress(self, size, key):
        if key == 'j':
            self._baseline = self._baseline + 1
            key = None
        elif key == 'k':
            self._baseline = self._baseline - 1
            key = None

        return super(CRScrollArea, self).keypress(size, key)
