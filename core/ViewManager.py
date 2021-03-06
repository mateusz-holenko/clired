_views = []
loop = None


def get_current_view():
    if not _views:
        return None
    else:
        return _views[-1]


def show_view(view):
    _views.append(view)
    if loop is not None:
        loop.widget.set_body(get_current_view())


def close_view():
    _views.pop()
    v = get_current_view()
    if v is not None:
        loop.widget.set_body(v)
        return True
    else:
        return False


def replace_view(view):
    close_view()
    show_view(view)


def is_last_view():
    return len(_views) == 1


def get_commandbar():
    if loop is not None:
        return loop.widget.get_footer()
    else:
        return None

def set_commandbar(widget):
    if loop is not None:
        loop.widget.set_footer(widget)
