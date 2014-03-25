import random
import time


_authors = [
    "Jon Doe",
    "Clare Rigg",
    "Karen Denton",
    "Ignacio Dyer",
    "Duane Cieslak",
    "Dominic Liang"
]

_statuses = [
    "New",
    "In Progress",
    "Closed"
]

_priorities = [
    "Low",
    "Normal",
    "High",
    "Urgent"
]


def get_fake(amount):
    result = []
    for i in range(amount):
        fake = CRFakeIssue()
        fake.id = 3000 + i
        fake.tracker = "Bug"
        fake.status.name = random.choice(_statuses)
        fake.priority.name = random.choice(_priorities)
        fake.category.name = "TUI"
        fake.fixed_version.name = "2014-03"
        fake.subject = "Subject of fake issue #" + str(fake.id)
        fake.author.name = random.choice(_authors)
        fake.assigned_to.name = random.choice(_authors)
        fake.done_ratio = random.randint(0, 100)
        fake.description = "Details f2f'ed"

        result.append(fake)
    return result


class CRFakeIssue(object):

    def __init__(self):
        self.author = CRFakeObject()
        self.assigned_to = CRFakeObject()
        self.fixed_version = CRFakeObject()
        self.category = CRFakeObject()
        self.priority = CRFakeObject()
        self.status = CRFakeObject()


class CRFakeObject(object):
    pass


def redmineImportThreadsFake(redmine, view, loop, main):
    main.status.info("Downloading issues...")
    time.sleep(1)  # there is a race to find...
    for issue in CRFakeIssue.get_fake(100):
        view.add(issue)
    main.status.success("Download completed.")
    loop.draw_screen()

if __name__ == "__main__":
    for f in get_fake(3):
        print(f.__dict__)
