import urwid
import math


class CRListBox(urwid.ListBox):

    def __init__(self, arg):
        super(CRListBox, self).__init__(arg)

    def count(self):
        return len(self.body)

    def first_visible_index(self, size):
        offset = self.get_focus_offset_inset(size)[0]
        height = size[1]

        if offset - height == 0:
            return self.focus_position - height + 1
        elif offset == 0:
            return self.focus_position + 1
        else:
            return self.focus_position - offset + 1

    def last_visible_index(self, size):
        return self.first_visible_index(size) + size[1] - 2

    def focus_next(self, size):
        try:
            self.set_focus(self.focus_position + 1, 'above')
            return True
        except:
            return False

    def focus_prev(self, size):
        try:
            self.set_focus(self.focus_position - 1, 'below')
            return True
        except:
            return False

    def focus_next_page(self, size):
        try:
            self.set_focus(self.focus_position + size[1], 'above')
            self.set_focus_valign('top')
            return True
        except:
            return False

    def focus_prev_page(self, size):
        try:
            self.set_focus(self.focus_position - size[1], 'below')
            self.set_focus_valign('top')
            return True
        except:
            return False
