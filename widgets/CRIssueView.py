import urwid
import logging
from widgets.CRTable import CRFlowTable

logger = logging.getLogger(__name__)


class CRIssueView(urwid.Frame):

    def __init__(self, issue):
        self._issue = issue
        self._header = urwid.Text("{0} #{1}: {2}".format(issue.tracker, issue.id, issue.subject))

        pile = []
        pile.append(urwid.Divider('-'))
        pile.append(urwid.Text("Added by {0} {1} ago. Updated {1} ago.".format(issue.author.name, "long long time")))
        pile.append(urwid.Text(''))

        table = CRFlowTable([15, 0, 15, 0])
        table.add(["Status:", issue.status.name, "Start date:", "???"])
        table.add(["Priority:", issue.priority.name, "Due date:", "???"])
        table.add(["Assignee:", issue.assigned_to.name, "% Done:", urwid.ProgressBar('issue-progress_completed', 'issue-progress_incompleted', current=issue.done_ratio)])
        table.add(["Category:", issue.category.name, "Spent time:", "-"])
        table.add(["Target", issue.fixed_version.name, "", ""])
        table.add(["Resolution:", "???", "", ""])

        pile.append(table)
        pile.append(urwid.Divider('-'))
        pile.append(urwid.Text(issue.description))

        super(CRIssueView, self).__init__(urwid.ListBox(pile), header=self._header)

    def keypress(self, size, key):
        logger.debug("Key pressed: " + str(key))

        if key == 'q' and hasattr(self, 'on_quit'):
            self.on_quit()
            key = None

        super(CRIssueView, self).keypress(size, key)
