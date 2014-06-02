from core.View import View
import urwid
import core.Signals


class MyPageView(View):

    def __init__(self, issues):
        core.Signals.register_signal(self, 'selected')
        self._widget = MyPageList(urwid.SimpleListWalker([MyPageItem(issue) for issue in issues]))
        urwid.signals.connect_signal(self._widget, 'selected', self._issue_selected)

    def get_widget(self):
        return self._widget

    def key_pressed(self, key):
        return False

    def _issue_selected(self, issue):
        core.Signals.emit_signal(self, 'selected', issue)


class MyPageList(urwid.ListBox):

    def __init__(self, args):
        core.Signals.register_signal(self, 'selected')
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
        elif key == 'enter':
            core.Signals.emit_signal(self, 'selected', self.focus.value())
            pass
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
