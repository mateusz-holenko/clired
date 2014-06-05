import urwid
import urwid.signals

_registered_signals = {}


def register_signal(obj, name):
    if obj.__class__ not in _registered_signals:
        _registered_signals[obj.__class__] = []
    if name not in _registered_signals[obj.__class__]:
        _registered_signals[obj.__class__].append(name)
        urwid.register_signal(obj.__class__, _registered_signals[obj.__class__])


def emit_signal(obj, name, args):
    register_signal(obj, name)
    urwid.emit_signal(obj, name, args)
