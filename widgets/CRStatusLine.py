import urwid


class CRStatusLine(urwid.Text):

    def warning(self, text):
        self.set_text(('status_line-warning', text))

    def error(self, text):
        self.set_text(('status_line-error', text))

    def info(self, text):
        self.set_text(('status_line-info', text))

    def success(self, text):
        self.set_text(('status_line-success', text))
