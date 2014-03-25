import logging

logger = logging.getLogger(__name__)


class settings(object):

    def __init__(self):
        self._dict = {}
        pass

    def value(self, name, default=None):
        return self._dict.get(name, default)

    def set_value(self, name, value):
        logger.debug("Variable {0} set to {1}".format(name, value))
        self._dict[name] = value

    def read(self, file):
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
