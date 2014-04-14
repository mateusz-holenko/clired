import urwid
import utils


class CRIssueJournal(urwid.ListBox):

    def __init__(self, issue):
        self._content = []

        for journal in issue.journals:
            self._content.append(CRIssueJournalListItem(journal))

        super(CRIssueJournal, self).__init__(urwid.SimpleFocusListWalker([]))

    def render(self, size, focus=False):
        self.body.clear()
        if len(self._content) == 0:
            self.body.append(urwid.Text("Journal is empty"))
        else:
            for item in self._content:
                canvas = item.render((size[0],), focus)
                for line in canvas.text:
                    self.body.append(urwid.Text(line))
                self.body.append(urwid.Text(''))
                self.body.append(urwid.Text(''))

        return super(CRIssueJournal, self).render(size, focus)


class CRIssueJournalListItem(urwid.Columns):

    def __init__(self, journalItem):

        author_and_date = [urwid.Text(journalItem.user.name), urwid.Text("{0}".format(journalItem.created_on))]

        details_and_notes = []
        if len(journalItem.details) > 0:
            for detail in journalItem.details:
                details_and_notes.append(CRIssueJournalItemDetail(detail))
            details_and_notes.append(urwid.Text(''))
        details_and_notes.append(urwid.Text(journalItem.notes))

        super(CRIssueJournalListItem, self).__init__([(25, urwid.Pile(author_and_date)), (urwid.Pile(details_and_notes))])


class CRIssueJournalItemDetail(urwid.Text):

    def __init__(self, detail):
        name = detail['name']
        newv = str(detail['new_value'])
        
        provider = utils.CRRedmineProvider.get_provider()
        resolver = {
            'status_id': ('Status', provider.issue_status),
            'priority_id': ('Priority', provider.issue_priority)
        }

        if 'old_value' in detail:
            oldv = str(detail['old_value'])

            if detail['name'] in resolver:
                name = resolver[detail['name']][0]
                oldv = resolver[detail['name']][1](detail['old_value'])
                newv = resolver[detail['name']][1](detail['new_value'])

            super(CRIssueJournalItemDetail, self).__init__("{0} changed from {1} to {2}".format(name, oldv, newv))
        else:

            if detail['name'] in resolver:
                name = resolver[detail['name']][0]
                newv = resolver[detail['name']][1](detail['new_value'])

            super(CRIssueJournalItemDetail, self).__init__("{0} set to {1}".format(name, newv))
