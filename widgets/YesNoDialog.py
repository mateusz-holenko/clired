import urwid
import core.Signals

class YesNoDialog(urwid.Text):

    def __init__(self, text):
        core.Signals.register_signal(self, 'dialog_finished')
        super(YesNoDialog, self).__init__("{0} [Yy/Nn]".format(text))

    def keypress(self, key):
        if key == 'y' or key == 'Y':
            core.Signals.emit_signal(self, 'dialog_finished', True)
        elif key == 'n' or key == 'N':
            core.Signals.emit_signal(self, 'dialog_finished', False)
