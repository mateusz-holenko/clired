from widgets.CRListBox import CRListBox
import re
import urwid
import logging

logger = logging.getLogger(__name__)


class CRIssuesList(CRListBox):

    def __init__(self):
        self.__walker = urwid.SimpleFocusListWalker([])
        self.__formatter = CRIssueLineFormatter("%i %a %A %100T")
        super(CRIssuesList, self).__init__(self.__walker)

    def keypress(self, size, key):
        logger.debug("Key pressed: " + str(key))
        if key == 'j':
            self.focus_next(size)
        elif key == 'k':
            self.focus_prev(size)
        elif key == 'page down':
            self.focus_next_page(size)
            key = None
        elif key == 'page up':
            self.focus_prev_page(size)
            key = None
        elif key == 'enter':
            #if hasattr(self, 'on_issue_selected'):
            self.on_issue_selected(self.focus.issue)
            #key = None

        return super(CRIssuesList, self).keypress(size, key)

    def add(self, issue):
        self.__walker.append(CRIssueItem(issue, self.__formatter))

    def size(self):
        return len(self.__walker)


class CRIssueItem(urwid.AttrMap):

    def __init__(self, issue, formatter):
        self.issue = issue
        super(CRIssueItem, self).__init__(urwid.Text(formatter.process(issue)), 'issues_index-normal', 'issues_index-focused')


class CRIssueLineFormatter(object):
    """
    Represents issue line description.

    The line is interpreted as a normal string with the exception of special formatting characters:
        %% - percantage sign (escaped)
        %i - id
        %t - tracker (bug, feature, enhancement, etc.)
        %s - status (new, closed, in progress, etc.)
        %p - priority (low, normal, urgent, etc.)
        %a - author
        %A - assigned to
        %c - category
        %v - fixed version
        %P - parent task
        %T - subject
        %d - description
        %S - start date
        %r - done ration
        %C - created on
        %U - updated on
    """
    def __init__(self, format):
        self.__format = format
        self.__fields = dict([
            ('i', (4,  'id')),
            ('t', (3,  'tracker.name')),
            ('s', (5,  'status.name')),
            ('p', (7,  'priority.name')),
            ('a', (20, 'author.name')),
            ('A', (20, 'assigned_to.name')),
            ('c', (7,  'category.name')),
            ('v', (7,  'fixed_version.name')),
            ('P', (4,  'parent["id"]')),
            ('T', (30, 'subject')),
            ('d', (10, 'description')),
            ('S', (7,  'start_date')),  # formatting
            ('r', (3,  'done_ratio')),
            ('C', (6,  'created_on')),  # formatting
            ('U', (6,  'updated_on')),  # formatting
        ])

    def process(self, issue):
        line = ''
        previous_location = 0
        pattern = re.compile("(?<!%)(?:%%)*(?P<all>%(?P<caps>!?)(?P<count>[0-9]*)(?P<index>[a-zA-Z]))")
        for match in pattern.finditer(self.__format):
            index = match.group("index")
            if index not in self.__fields:
                continue

            line += self.__format[previous_location:match.start()]
            caps = match.group("caps") == '!'
            count = int(match.group("count")) if match.group("count") != '' else self.__fields[index][0]

            value = str(eval('issue.' + self.__fields[index][1]))
            if len(value) > count:
                value = value[:count]
            else:
                value = value.ljust(count, ' ')

            if caps:
                value = value.upper()

            line += value
            previous_location = match.start() + len(match.group("all"))
        return line
