_buffer = []
_bindings = {}


def bind(keys, context, action):
    if context not in _bindings:
        _bindings[context] = {}
    _bindings[context][keys] = action


def map(key, context):
    global _buffer
    _buffer.append(key)

    if context not in _bindings:
        _buffer = []
        return None

    flag = False
    for b in _bindings[context]:
        p = common_prefix(b, ''.join(_buffer))
        if p == len(b):
            _buffer = []
            return _bindings[context][b]
        elif p != 0:
            flag = True

    if flag:
        return '_MORE'
    else:
        _buffer = []
        return None


def common_prefix(l1, l2):
    size = min(len(l1), len(l2))
    for i in range(0, size):
        if l1[i] != l2[i]:
            return i
    return size

bind('sm', 'IssuesView', 'SHOW_MY_ISSUES')
bind('sam', 'IssuesView', 'SHOW_ALL_MY_ISSUES')
bind('si', 'IssuesView', 'SHOW_ISSUES')
bind('sai', 'IssuesView', 'SHOW_ALL_ISSUES')
bind('gg', 'IssuesView', 'GOTO_TOP')
bind('G', 'IssuesView', 'GOTO_BOTTOM')
