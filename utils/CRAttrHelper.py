import logging

logger = logging.getLogger(__name__)


def attribute(obj, name, default):
    if obj is not None and hasattr(obj, name):
        result = getattr(obj, name, default)
        return result if result is not None else default
    else:
        return default
