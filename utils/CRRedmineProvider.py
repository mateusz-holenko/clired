from redmine import Redmine


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
        handler(project.issues)

    def set_status_handler(self, status):
        self._status = status
