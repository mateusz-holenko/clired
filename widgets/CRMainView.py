import urwid
import logging
from widgets.CRStatusLine import CRStatusLine
from widgets.CRIssuesView import CRIssuesView
from widgets.CRIssueView import CRIssueView

logger = logging.getLogger(__name__)


class CRMainView(urwid.Frame):

    def __init__(self, provider):
        self.__content = urwid.Filler(urwid.Text(""))
        self.status = CRStatusLine('')
        self._issues_view = CRIssuesView(provider)
        self._issues_view.set_selection_handler(self.show_issue)

        super(CRMainView, self).__init__(self.__content, None, self.status)
        self.show_issues()

    def show_issues(self):
        self.set_body(self._issues_view)
        self.current = self._issues_view

    def show_issue(self, issue):
        self.current = CRIssueView(issue)
        self.current.on_quit = self._quit_issue_handler
        self.set_body(self.current)

    def _quit_issue_handler(self):
        self.show_issues()

    def keypress(self, size, key):
        logger.debug("Key pressed: " + str(key))

        return super(CRMainView, self).keypress(size, key)
