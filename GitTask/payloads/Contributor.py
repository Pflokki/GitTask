from GitTask.RequestMaker import RequestMaker


class Contributor:
    def __init__(self, login, contributions):
        self.login = login
        self.contributions = contributions


class ContributorConvertor:
    @staticmethod
    def list_convertor(c_data: list) -> list:
        contributors = []
        for user in c_data:
            t_contributor = Contributor(
                user.get('login', 'unnamed'),
                user.get('contributions', -1)
            )
            contributors.append(t_contributor)
        return contributors


class ContributorRequestMaker(RequestMaker):
    def __init__(self, **kwargs):
        super().__init__()

        self.url = f"https://api.github.com/repos/{kwargs['owner']}/{kwargs['repo']}/contributors"
        self.params = {
                          'from': kwargs['date_from'],
                          'to': kwargs['date_to']
                      }
