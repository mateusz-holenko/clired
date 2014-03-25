import urwid
import logging
from widgets.CRIssuesList import CRIssuesList

logger = logging.getLogger(__name__)


class CRIssuesView(urwid.Frame):

    def __init__(self, provider):
        self._table = CRIssuesList()
        self._footer = urwid.Text('')
        self._rendered = False
        self._provider = provider

        super(CRIssuesView, self).__init__(self._table, None, self._footer)

    def render(self, size, focus=False):
        if self._rendered is False:
            self._rendered = True
            self._provider.issues(self.add_range)

        count = self._table.count()
        if count == 0:
            self._footer.set_text("No issues found")
        else:
            start = self._table.first_visible_index(size)
            end = self._table.last_visible_index(size)
            self._footer.set_text("Issues from {0} to {1} of {2}.".format(start, end, count))

        return super(CRIssuesView, self).render(size, focus)

    def keypress(self, size, key):
        logger.debug("Key pressed: " + str(key))
        return super(CRIssuesView, self).keypress(size, key)

    def add_range(self, issues):
        for i in issues:
            self.add(i)

    def add(self, issue):
        self._table.add(issue)

    def clear(self):
        self._table.clear()

    def set_selection_handler(self, handler):
        self._table.on_issue_selected = handler
