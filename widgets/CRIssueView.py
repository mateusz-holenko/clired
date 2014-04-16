import urwid
import logging
from widgets.CRTable import CRFlowTable
from widgets.CRScrollArea import CRScrollArea
#import utils.CRRedmineProvider
from widgets.CRIssueJournal import CRIssueJournal

logger = logging.getLogger(__name__)


class CRIssueView(urwid.Frame):

    def __init__(self, issue):
        self._issue = issue
        self._header = CRIssueHeader(issue)

        #self.focus_position = 'body'
        super(CRIssueView, self).__init__(CRScrollArea(CRIssueDescription(issue)), header=self._header)
        #self.focus_position = 'body'

    def keypress(self, size, key):
        logger.debug("Key pressed: " + str(key))

        if key == 'q' and hasattr(self, 'on_quit'):
            self.on_quit()
        elif key == 'h':
            #self.focus_position = 'header'
            self._toggle_header()
            #self.focus_position = 'body'
        elif key == 'D':
            #self.focus_position = 'body'
            self._show_description()
        elif key == 'n':
            #self.focus_position = 'body'
            self._show_journal()
        else:
            super(CRIssueView, self).keypress(size, key)

        self._invalidate()

    def _toggle_header(self):
        logger.debug("Header toggled")
        self._header = CRIssueHeader(self._issue, not self._header.is_meta_visible())
        self._header._invalidate()

    def _show_description(self):
        logger.debug("Description shown")
        self._body = CRScrollArea(CRIssueDescription(self._issue))
        self._body._invalidate()

    def _show_journal(self):
        logger.debug("Journal shown")
        self._body = CRScrollArea(CRIssueJournal(self._issue))
        self._body._invalidate()


class CRIssueHeader(urwid.Pile):

    def __init__(self, issue, show_meta=True):
        content = []
        content.append(urwid.Text("{0} #{1}: {2}".format(issue.tracker, issue.id, issue.subject)))
        content.append(urwid.Divider('-'))
        if show_meta:
            content.append(CRIssueMeta(issue))
            content.append(urwid.Divider('-'))

        self._is_meta_visible = show_meta
        super(CRIssueHeader, self).__init__(content)

    def is_meta_visible(self):
        return self._is_meta_visible


class CRIssueMeta(urwid.Pile):

    def __init__(self, issue):

        status         = getattr(getattr(issue, 'status', None), 'name', '-')
        start_date     = str(getattr(issue, 'start_date', '-'))
        priority       = getattr(getattr(issue, 'priority', None), 'name', '-')
        due_date       = getattr(issue, 'due_date', '-')
        assigned_to    = getattr(getattr(issue, 'assigned_to', None), 'name', '-')
        done_ratio     = getattr(issue, 'done_ratio', '-')
        category       = getattr(getattr(issue, 'category', None), 'name', '-')
        spent_time     = getattr(issue, 'spent_hours', '-')
        target_version = getattr(getattr(issue, 'fixed_version', None), 'name', '-')

        table = CRFlowTable([15, 0, 15, 0])
        table.add(["Status:", status, "Start date:", start_date])
        #table.add(["Priority:", priority, "Due date:", due_date])
        table.add(["Assignee:", assigned_to, "% Done:", "{0} %".format(done_ratio)])
        #table.add(["Category:", category, "Spent time:", spent_time])
        table.add(["Target:", target_version, "", ""])

        if hasattr(issue, 'custom_fields') and issue.custom_fields is not None:
            for cf in issue.custom_fields:
                value = getattr(cf, 'value')
                table.add(["{0}:".format(cf.name), value if value is not None else '-', "", ""])

        pile = [
            urwid.Text("Added by {0} {1} ago. Updated {1} ago.".format(issue.author.name, "long long time")),
            urwid.Text(''),
            table
        ]

        super(CRIssueMeta, self).__init__(pile)


class CRIssueDescription(urwid.ListBox):

    def __init__(self, issue):
        walker = urwid.SimpleFocusListWalker([urwid.Text(l) for l in issue.description.splitlines()])
        super(CRIssueDescription, self).__init__(walker)


#class CRIssueJournal(urwid.Pile):
#
#    def __init__(self, issue):
#        content = []
#        if hasattr(issue, 'journals'):
#            for item in issue.journals:
#                content.append(CRIssueJournalItem(item))
#
#        super(CRIssueJournal, self).__init__(content)
#
#
#class CRIssueJournalItem(urwid.Pile):
#
#    def __init__(self, item):
#        content = []
#        content.append(urwid.Text("Updated by {0} {1} ago.".format(item.user.name, item.created_on)))
#        for detail in item.details:
#            content.append(CRIssueJournalItemDetail(detail))
#        content.append(urwid.Text(item.notes))
#
#        content.append(urwid.Text(''))
#        super(CRIssueJournalItem, self).__init__(content)
#
#
#class CRIssueJournalItemDetail(urwid.Text):
#
#    def __init__(self, detail):
#        name = detail['name']
#        oldv = str(detail['old_value'])
#        newv = str(detail['new_value'])
#
#        provider = utils.CRRedmineProvider.get_provider()
#        resolver = {
#            'status_id': ('Status', provider.issue_status),
#            'priority_id': ('Priority', provider.issue_priority)
#        }
#
#        if detail['name'] in resolver:
#            name = resolver[detail['name']][0]
#            oldv = resolver[detail['name']][1](detail['old_value'])
#            newv = resolver[detail['name']][1](detail['new_value'])
#
#        super(CRIssueJournalItemDetail, self).__init__("{0} changed from {1} to {2}".format(name, oldv, newv))
#
#
#class CRIssueJournal2(urwid.Columns):
#
#    def __init__(self, issue):
#        items = [urwid.Text('{0}\n{1}'.format(item.user.name, item.created_on)) for item in issue.journals]
#
#        super(CRIssueJournal2, self).__init__([
#            urwid.ListBox(urwid.SimpleFocusListWalker(items))])
#            #urwid.ListBox(urwid.Frame(urwid.Text('pusto')))])
