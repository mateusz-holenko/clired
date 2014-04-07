from redmine import Redmine
import utils.CRSettings
import logging

__provider__ = None
logger = logging.getLogger(__name__)


def get_provider():
    global __provider__
    if __provider__ is None:
        __provider__ = CRRedmineProvider(utils.CRSettings.get_settings())
    return __provider__


class CRRedmineProvider(object):

    def __init__(self, settings):
        self._settings = settings
        self._redmine = Redmine(
            settings.value('server_uri'),
            username=settings.value('username'),
            password=settings.value('password'),
            requests=dict(verify=False))

    def issues(self, handler):
        if not hasattr(self, '_issues') or self._issues is None:
            self._status.info("Downloading issues...")
            project = self._redmine.project.get(self._settings.value('project'))
            self._issues = project.issues
            self._status.success("Download completed.")

        handler(self._issues)

    def issue(self, id):
        return self._redmine.issue.get(id)

    def issue_status(self, id):
        if not hasattr(self, '_statuses') or self._statuses is None:
            self._statuses = self._redmine.issue_status.all()

        return self._statuses.get(id).name

    def issue_priority(self, id):
        if not hasattr(self, '_priorities') or self._priorities is None:
            self._priorities = self._redmine.enumeration.filter(resource='issue_priorities')

        return self._priorities.get(id).name

    def set_status_handler(self, status):
        self._status = status
