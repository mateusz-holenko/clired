import urwid


class CRScrollArea(urwid.BoxWidget):

    def __init__(self, content):
        self._content = content
        self._baseline = 0

    def render(self, size, focus=False):
        return self._content.render(size, focus)
#        fake_size = (size[0], size[1] + self._baseline)
#        canvas = urwid.CompositeCanvas(self._content.render(fake_size, focus))
#        canvas.trim(self._baseline, None)
#        return canvas
#
    def keypress(self, size, key):
        if key == 'j':
            key = 'down'
        elif key == 'k':
            key = 'up'

        self._content.keypress(size, key)
        #if key == 'j':
        #    if self._baseline < size[1]:
        #        self._baseline = self._baseline + 1
        #    key = None
        #elif key == 'k':
        #    if self._baseline > 0:
        #        self._baseline = self._baseline - 1
        #    key = None

        #self._invalidate()
