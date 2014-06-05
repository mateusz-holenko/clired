from core.View import View
import core.ViewManager
import urwid
import core.Signals


class MyPageView(View):

    def __init__(self, issues):
        core.Signals.register_signal(self, 'selected')
        core.Signals.register_signal(self, 'goto_issue')

        self._widget = MyPageList(urwid.SimpleListWalker([MyPageItem(issue) for issue in issues]))
        self._goto = TaskGotoBar()

    def get_widget(self):
        return self._widget

    def key_pressed(self, key):
        if self._goto.handle_key(key):
            return True
        elif key == 'enter':
            val = self._goto.get_value()
            if val is not None:
                self._goto.clear()
                core.Signals.emit_signal(self, 'goto_issue', val)
                pass
            else:
                core.Signals.emit_signal(self, 'selected', self._widget.focus.value())
            return True

        return False


class TaskGotoBar:
    def __init__(self):
        self._buffer = []

    def handle_key(self, key):
        if key >= '0' and key <= '9':
            self._buffer.append(key)
        elif key == 'esc':
            self._buffer = []
        elif key == 'backspace':
            if len(self._buffer) > 0:
                self._buffer.pop()
        else:
            return key != 'enter' and len(self._buffer) > 0

        val = self.get_value()
        if val is not None:
            core.ViewManager.get_commandbar().set_text("Goto issue: " + str(val))
        else:
            core.ViewManager.get_commandbar().set_text("")

        return True

    def get_value(self):
        if len(self._buffer) == 0:
            return None
        else:
            return int(''.join(self._buffer))

    def clear(self):
        self._buffer = []
        core.ViewManager.get_commandbar().set_text("")


class MyPageList(urwid.ListBox):

    def __init__(self, args):
        super(MyPageList, self).__init__(args)

    def keypress(self, size, key):
        if key == 'down' or key == 'j':
            if self.focus_position < len(self.body) - 1:
                self.set_focus(self.focus_position + 1, 'above')
        elif key == 'up' or key == 'k':
            if self.focus_position > 0:
                self.set_focus(self.focus_position - 1, 'below')
        elif key == 'g':
            self.set_focus(0)
        elif key == 'G':
            self.set_focus(len(self.body) - 1)
        else:
            return key


class MyPageItem(urwid.AttrMap):
    def __init__(self, issue):
        self._issue = issue
        columns = urwid.Columns(
            [(6, urwid.Text(str(issue.id))),
             (6, urwid.Text(issue.tracker.name, wrap='clip')),
             (2, urwid.Text('')),
             (7, urwid.Text(issue.priority.name, wrap='clip')),
             (2, urwid.Text('')),
             (10, urwid.Text(issue.status.name, wrap='clip')),
             (2, urwid.Text('')),
             (urwid.Text(issue.subject, wrap='clip'))])

        super(MyPageItem, self).__init__(columns, 'issues_index-normal', 'issues_index-focused')

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

    def value(self):
        return self._issue
