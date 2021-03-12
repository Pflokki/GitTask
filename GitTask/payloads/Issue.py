import datetime
from GitTask.RequestMaker import RequestMaker


class IssueRequestMaker(RequestMaker):
    url = "https://api.github.com/search/issues"

    def __init__(self, query):
        super().__init__()
        self.params = {
            'q': query,
        }

    def run(self):
        self.url_2 = "123"


class IssueQueryMaker:
    @staticmethod
    def opened_issue(**kwargs):

        return f"is:issue " \
               f"repo:{kwargs['owner']}/{kwargs['repo']} " \
               f"state:open " \
               f"created:<{kwargs['date_to']} " \
               f"created:>={kwargs['date_from']}"

    @staticmethod
    def closed_issue(**kwargs):
        return f"is:issue " \
               f"repo:{kwargs['owner']}/{kwargs['repo']} " \
               f"state:closed " \
               f"created:<{kwargs['date_to']} " \
               f"created:>={kwargs['date_from']}"

    @staticmethod
    def old_issue(**kwargs):
        old_max_date = datetime.date.today() - datetime.timedelta(days=14)
        date_to = min(old_max_date, kwargs['date_to'])
        return f"is:issue " \
               f"repo:{kwargs['owner']}/{kwargs['repo']} " \
               f"state:open " \
               f"created:<{date_to.strftime('%Y-%m-%d')} " \
               f"created:>={kwargs['date_from']}"
