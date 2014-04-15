import urwid
import logging
from widgets.CRTable import CRFlowTable
from widgets.CRScrollArea import CRScrollArea
#import utils.CRRedmineProvider
from widgets.CRIssueJournal import CRIssueJournal
from utils.CRAttrHelper import attribute

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

        status         = attribute(attribute(issue, 'status', None), 'name', '-')
        start_date     = str(attribute(issue, 'start_date', '-'))
        priority       = attribute(attribute(issue, 'priority', None), 'name', '-')
        due_date       = attribute(issue, 'due_date', '-')
        assigned_to    = attribute(attribute(issue, 'assigned_to', None), 'name', '-')
        done_ratio     = attribute(issue, 'done_ratio', '-')
        category       = attribute(attribute(issue, 'category', None), 'name', '-')
        spent_time     = str(attribute(issue, 'spent_hours', '-'))
        target_version = attribute(attribute(issue, 'fixed_version', None), 'name', '-')
        logger.debug("Priority is {0}".format(due_date))

        table = CRFlowTable([15, 0, 15, 0])
        table.add(["Status:", status, "Start date:", start_date])
        table.add(["Priority:", priority, "Due date:", due_date])
        table.add(["Assignee:", assigned_to, "% Done:", "{0} %".format(done_ratio)])
        table.add(["Category:", category, "Spent time:", spent_time])
        table.add(["Target:", target_version, "", ""])

        if hasattr(issue, 'custom_fields'):
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
