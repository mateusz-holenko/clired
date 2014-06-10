import redmine
import logging

import core.Configuration

__provider__ = None
logger = logging.getLogger(__name__)


def instance():
    global __provider__
    if __provider__ is None:
        __provider__ = Redmine(core.Configuration.instance())
    return __provider__


class Redmine(object):

    def __init__(self, settings):
        self._settings = settings
        self._redmine = redmine.Redmine(
            settings.value('server_uri'),
            username=settings.value('username'),
            password=settings.value('password'),
            requests=dict(verify=False),
            raise_attr_exception=False)

    def project(self):
        if not hasattr(self, '_project') or self._project is None:
            self._project = self._redmine.project.get(self._settings.value('project'))
        return self._project

    def my_issues(self, show_closed=False):
        if not hasattr(self, '_my_issues') or self._my_issues is None:
            self._my_issues = {}
        if show_closed not in self._my_issues:
            self._my_issues[show_closed] = self._redmine.issue.filter(assigned_to_id='me', status_id='open' if not show_closed else '*')
        return self._my_issues[show_closed]

    def issues(self, show_closed=False):
        if not hasattr(self, '_issues') or self._issues is None:
            self._issues = self.project().issues
        return self._issues

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

    def tracker(self, id):
        if not hasattr(self, '_trackers') or self._trackers is None:
            self._trackers = self._redmine.tracker.all()

        return self._trackers.get(id).name

    def target_version(self, id):
        if not hasattr(self, '_targets') or self._targets is None:
            project = self._redmine.project.get(self._settings.value('project'))
            self._targets = project.versions

        return self._targets.get(id).name

    def user(self, id):
        if not hasattr(self, '_users') or self._users is None:
            self._users = {}
        if not id in self._users:
            self._users[id] = self._redmine.user.get(id)
        return "{0} {1}".format(self._users[id].firstname, self._users[id].lastname)

    def set_status_handler(self, status):
        self._status = status
