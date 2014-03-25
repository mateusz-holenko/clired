import urwid


class CRTable(urwid.ListBox):
    """
    Table widget.

    Private attributes:
        _columns
            List of columns formats where every column can be described as:
                * positiver integer - column with fixed width
                * intger of value 0 - column with auto width
        _walker
    """

    def __init__(self, columns):
        self._columns = columns
        self._walker = urwid.SimpleFocusListWalker([])
        super(CRTable, self).__init__(self._walker)

    def add(self, cells):
        if len(cells) != len(self._columns):
            raise Exception("Wrong cell amount")

        result = []
        for i, column in enumerate(self._columns):
            content = urwid.Text(cells[i]) if isinstance(cells[i], str) else cells[i]
            if column == 0:
                result.append(content)
            else:
                result.append((column, content))

        self._walker.append(urwid.Columns(result))


class CRFlowTable(urwid.FlowWidget):

    def __init__(self, columns):
        self._table = CRTable(columns)

    def add(self, cells):
        self._table.add(cells)

    def render(self, size, focus=False):
        return self._table.render((size[0], self.rows(size, focus)), focus)

    def rows(self, size, focus=False):
        return sum([r.rows(size, focus) for r in self._table._walker])
