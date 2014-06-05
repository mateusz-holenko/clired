import urwid
import core


class IssueView(urwid.Frame):

    def __init__(self, issue):
        self._issue = issue
        super(IssueView, self).__init__(MetadataElement(self._issue), header=HeaderElement(self._issue))

    def keypress(self, size, key):
        if key == 'm':
            self.set_body(MetadataElement(self._issue))
        elif key == 'd':
            self.set_body(DescriptionElement(self._issue))
        elif key == 'n':
            self.set_body(JournalElement(self._issue))
        elif key == 'a':
            self.set_body(AttachmentsElement(self._issue))
        elif key == 'w':
            self.set_body(WatchersElement(self._issue))
        else:
            return key


class HeaderElement(urwid.Pile):
    def __init__(self, issue):
        content = []
        content.append(urwid.Divider('-'))
        content.append(urwid.Text("{0} #{1}: {2}".format(issue.tracker, issue.id, issue.subject)))
        content.append(urwid.Divider('-'))
        super(HeaderElement, self).__init__(content)


class DescriptionElement(urwid.ListBox):
    def __init__(self, issue):
        if issue.description:
            walker = urwid.SimpleFocusListWalker([urwid.Text(l) for l in issue.description.splitlines()])
        else:
            walker = urwid.SimpleFocusListWalker([urwid.Text(":: No description provided ::")])
        super(DescriptionElement, self).__init__(walker)


class MetadataElement(urwid.ListBox):
    def __init__(self, issue):
        items = {}
        items['Status'] =     self.resolve(issue, 'status', 'name')
        items['Start date'] = self.resolve(issue, 'start_date')
        items['Priority'] =   self.resolve(issue, 'priority', 'name')
        items['Due date'] =   self.resolve(issue, 'due_date')
        items['Assignee'] =   self.resolve(issue, 'assigned_to', 'name')
        items['% Done'] =     self.resolve(issue, 'done_ratio')
        items['Category'] =   self.resolve(issue, 'category', 'name')
        items['Spent time'] = self.resolve(issue, 'spent_hours')
        items['Target'] =     self.resolve(issue, 'fixed_version', 'name')
        items['Author'] =     self.resolve(issue, 'author', 'name')
        items['Created'] =    self.resolve(issue, 'created_on')
        items['Updated'] =    self.resolve(issue, 'updated_on')

        order = ['Status', 'Priority', 'Author', 'Assignee', '',
                 'Created', 'Updated', '',
                 'Start date', 'Due date', '% Done', 'Spent time', '',
                 'Category', 'Target', '']

        content = []
        width = 15

        for element in order:
            if element == "":
                content.append(urwid.Text(""))
            else:
                content.append(urwid.Columns([(width, urwid.Text(element + ":")), (urwid.Text(items[element]))]))

        if hasattr(issue, 'custom_fields') and issue.custom_fields is not None:
            for cf in issue.custom_fields:
                value = self.resolve(cf, 'value')
                content.append(urwid.Columns([(width, urwid.Text(cf.name + ":")), (urwid.Text(value))]))

        super(MetadataElement, self).__init__(urwid.SimpleFocusListWalker(content))

    def resolve(self, issue, *args):
        curr = issue
        for a in args:
            if hasattr(curr, a):
                curr = getattr(curr, a)
            else:
                return "-"

        return str(curr)


class JournalElement(urwid.ListBox):
    def __init__(self, issue):

        content = []
        if len(issue.journals) > 0:
            for journal in issue.journals:
                content.append(JournalItem(journal))
                content.append(urwid.Text(''))
        else:
            content.append(urwid.Text(":: Journal is empty ::"))

        super(JournalElement, self).__init__(urwid.SimpleFocusListWalker(content))


class JournalItem(urwid.Columns):
    def __init__(self, item):

        author_and_date = [urwid.Text(item.user.name), urwid.Text("{0}".format(item.created_on))]

        details_and_notes = []
        if len(item.details) > 0:
            for detail in item.details:
                details_and_notes.append(JournalItemDetail(detail))
            details_and_notes.append(urwid.Text(''))
        details_and_notes.append(urwid.Text(item.notes))

        super(JournalItem, self).__init__([(25, urwid.Pile(author_and_date)), (urwid.Pile(details_and_notes))])


class JournalItemDetail(urwid.Text):

    def __init__(self, detail):

        provider = core.Redmine.instance()
        resolver = {
            'status_id':        ('Status',         provider.issue_status),
            'priority_id':      ('Priority',       provider.issue_priority),
            'done_ratio':       ('% Done',         lambda x: str(x)),
            'tracker_id':       ('Tracker',        provider.tracker),
            'fixed_version_id': ('Target version', provider.target_version),
            'assigned_to_id':   ('Assignee',       provider.user)
        }

        dn = detail['name']

        name = dn
        newv = str(detail['new_value'])

        if dn in resolver:
            name = resolver[dn][0]
            newv = resolver[dn][1](newv)

        if 'old_value' in detail:
            oldv = str(detail['old_value'])

            if dn in resolver:
                oldv = resolver[dn][1](oldv)

            text = "{0} changed from {1} to {2}".format(name, oldv, newv)
        else:
            text = "{0} set to {1}".format(name, newv)

        super(JournalItemDetail, self).__init__(text)


class AttachmentsElement(urwid.ListBox):
    def __init__(self, issue):
        content = []
        if len(issue.attachments) == 0:
            content.append(urwid.Text(":: No attachments ::"))
        else:
            for att in issue.attachments:
                content.append(urwid.Columns(
                    [
                        (30, urwid.Text(att.filename)),
                        (15, urwid.Text(str(att.filesize))),
                        (15, urwid.Text(att.author.name)),
                        (urwid.Text(str(att.created_on)))
                    ]))
#content_url

        super(AttachmentsElement, self).__init__(urwid.SimpleFocusListWalker(content))


class WatchersElement(urwid.ListBox):
    def __init__(self, issue):
        content = []
        if len(issue.watchers) == 0:
            content.append(urwid.Text(":: No watchers ::"))
        else:
            content = [ urwid.Text(w.name) for w in issue.watchers ]

        super(WatchersElement, self).__init__(urwid.SimpleFocusListWalker(content))
