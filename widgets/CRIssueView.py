import urwid
import logging
from widgets.CRTable import CRFlowTable
from widgets.CRScrollArea import CRScrollArea
import utils.CRRedmineProvider
from widgets.CRIssueJournal import DoubleListBox

logger = logging.getLogger(__name__)


class CRIssueView(urwid.Frame):

    def __init__(self, issue):
        self._issue = issue
        self._header = CRIssueHeader(issue)

        super(CRIssueView, self).__init__(DoubleListBox(issue), header=self._header)

    def keypress(self, size, key):
        logger.debug("Key pressed: " + str(key))

        if key == 'q' and hasattr(self, 'on_quit'):
            self.on_quit()
            key = None

        super(CRIssueView, self).keypress(size, key)


class CRIssueHeader(urwid.Pile):

    def __init__(self, issue):
        content = []
        content.append(urwid.Text("{0} #{1}: {2}".format(issue.tracker, issue.id, issue.subject)))
        content.append(urwid.Divider('-'))
        content.append(CRIssueMeta(issue))
        content.append(urwid.Divider('-'))

        super(CRIssueHeader, self).__init__(content)


class CRIssueMeta(urwid.Pile):

    def __init__(self, issue):

        category = '-'  # issue.category.name if hasattr(issue, 'category') else '-'

        table = CRFlowTable([15, 0, 15, 0])
        table.add(["Status:", issue.status.name, "Start date:", "???"])
        table.add(["Priority:", issue.priority.name, "Due date:", "???"])
        #table.add(["Assignee:", issue.assigned_to.name, "% Done:", urwid.ProgressBar('issue-progress_completed', 'issue-progress_incompleted', current=issue.done_ratio)])
        table.add(["Assignee:", issue.assigned_to.name, "% Done:", "{0} %".format(issue.done_ratio)])
        table.add(["Category:", category, "Spent time:", "-"])
        #table.add(["Target", issue.fixed_version.name, "", ""])
        table.add(["Resolution:", "???", "", ""])

        pile = []

        pile.append(urwid.Text("Added by {0} {1} ago. Updated {1} ago.".format(issue.author.name, "long long time")))
        pile.append(urwid.Text(''))
        pile.append(table)

        super(CRIssueMeta, self).__init__(pile)


class CRIssueDescription(urwid.ListBox):

    def __init__(self, issue):
        self._walker = urwid.SimpleFocusListWalker([urwid.Text(l) for l in issue.description.splitlines()])
        super(CRIssueDescription, self).__init__(self._walker)


class CRIssueJournal(urwid.Pile):

    def __init__(self, issue):
        content = []
        if hasattr(issue, 'journals'):
            for item in issue.journals:
                content.append(CRIssueJournalItem(item))

        super(CRIssueJournal, self).__init__(content)


class CRIssueJournalItem(urwid.Pile):

    def __init__(self, item):
        content = []
        content.append(urwid.Text("Updated by {0} {1} ago.".format(item.user.name, item.created_on)))
        for detail in item.details:
            content.append(CRIssueJournalItemDetail(detail))
        content.append(urwid.Text(item.notes))

        content.append(urwid.Text(''))
        super(CRIssueJournalItem, self).__init__(content)


class CRIssueJournalItemDetail(urwid.Text):

    def __init__(self, detail):
        name = detail['name']
        oldv = str(detail['old_value'])
        newv = str(detail['new_value'])

        provider = utils.CRRedmineProvider.get_provider()
        resolver = {
            'status_id': ('Status', provider.issue_status),
            'priority_id': ('Priority', provider.issue_priority)
        }

        if detail['name'] in resolver:
            name = resolver[detail['name']][0]
            oldv = resolver[detail['name']][1](detail['old_value'])
            newv = resolver[detail['name']][1](detail['new_value'])

        super(CRIssueJournalItemDetail, self).__init__("{0} changed from {1} to {2}".format(name, oldv, newv))


class CRIssueJournal2(urwid.Columns):

    def __init__(self, issue):
        items = [urwid.Text('{0}\n{1}'.format(item.user.name, item.created_on)) for item in issue.journals]

        super(CRIssueJournal2, self).__init__([
            urwid.ListBox(urwid.SimpleFocusListWalker(items))])
            #urwid.ListBox(urwid.Frame(urwid.Text('pusto')))])
