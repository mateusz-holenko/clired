import logging
from os.path import expanduser

logger = logging.getLogger(__name__)
path = '{0}/.cliredrc'.format(expanduser('~'))

_settings = None


def get_settings():
    global _settings
    if _settings is None:
        _settings = CRSettings()
        try:
            _settings.read()
        except IOError:
            logger.warning("Error while reading configuration file: {0}".format(path))
    return _settings


class CRSettings(object):

    def __init__(self):
        self._dict = {}
        pass

    def value(self, name, default=None):
        return self._dict.get(name, default)

    def set_value(self, name, value):
        self._dict[name] = value

    def has_value(self, name):
        return name in self._dict

    def read(self, file=None):
        if file is None:
            file = path

        f = open(file, 'r')
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                # it is a comment line, continue
                continue
            elif line.startswith('set '):
                splitted = line[4:].split(' ')
                if len(splitted) != 2:
                    raise Exception("Error parsing configuration line: " + line)
                self.set_value(splitted[0], splitted[1])
            else:
                raise Exception("Error parsing configuration line: " + line)
