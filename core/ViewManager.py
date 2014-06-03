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
        loop.widget = get_current_view().get_widget()


def close_view():
    _views.pop()
    v = get_current_view()
    if v is not None:
        loop.widget = v.get_widget()
        return True
    else:
        return False
