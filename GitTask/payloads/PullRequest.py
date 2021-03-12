import datetime
from GitTask.RequestMaker import RequestMaker


class PullRequestRequestMaker(RequestMaker):
    def __init__(self, query):
        super().__init__()
        self.url = "https://api.github.com/search/issues"
        self.params = {
            'q': query,
        }


class PullRequestQueryMaker:
    @staticmethod
    def opened_pr(**kwargs):
        return f"is:pr " \
               f"repo:{kwargs['owner']}/{kwargs['repo']} " \
               f"state:open " \
               f"base:{kwargs['branch']} " \
               f"created:<{kwargs['date_to']} " \
               f"created:>={kwargs['date_from']} "

    @staticmethod
    def closed_pr(**kwargs):
        return f"is:pr " \
               f"repo:{kwargs['owner']}/{kwargs['repo']} " \
               f"state:closed " \
               f"base:{kwargs['branch']} " \
               f"created:<{kwargs['date_to']} " \
               f"created:>={kwargs['date_from']} "

    @staticmethod
    def old_pr(**kwargs):
        old_max_date = datetime.date.today() - datetime.timedelta(days=30)
        date_to = min(old_max_date, kwargs['date_to'])
        return f"is:pr " \
               f"repo:{kwargs['owner']}/{kwargs['repo']} " \
               f"state:open " \
               f"base:{kwargs['branch']} " \
               f"created:<{date_to.strftime('%Y-%m-%d')} " \
               f"created:>={kwargs['date_from']}"
