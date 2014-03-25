from .CRFakeIssue import get_fake
import widgets.CRIssuesList


def run():
    for i in get_fake(10):
        formatter = widgets.CRIssuesList.CRIssueLineFormatter("%i %a %A %T")
        print(formatter.process(i))
