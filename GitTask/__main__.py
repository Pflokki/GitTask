import json
from concurrent.futures import ThreadPoolExecutor

from GitTask.payloads.Contributor import ContributorConvertor, ContributorRequestMaker
from GitTask.payloads.Issue import IssueRequestMaker
from GitTask.payloads.PullRequest import PullRequestRequestMaker

from GitTask.payloads.Issue import IssueQueryMaker
from GitTask.payloads.PullRequest import PullRequestQueryMaker


from GitTask.RequestMaker import RequestMaker
from GitTask.RequestSender import RequestSender


def get_contributors(**kwargs):
    req = ContributorRequestMaker(**kwargs).get_request()

    resp = RequestSender.send(req)

    contributors = []
    if resp.status_code == 200:
        contributor_list = json.loads(resp.content)
        contributors = ContributorConvertor().list_convertor(contributor_list)
    return contributors


def get_values(request_maker: RequestMaker):
    request = request_maker.get_request()
    response = RequestSender.send(request)
    total_count = 0
    if response.status_code == 200:
        response_text: dict = json.loads(response.text)
        total_count = response_text.get('total_count', 0)

    return total_count


def run(owner, repo, branch, date_from, date_to):
    kwarg = {
        'owner': owner,
        'repo': repo,
        'branch': branch,
        'date_to': date_to,
        'date_from': date_from,
    }

    contributors = get_contributors(**kwarg)
    for index, contributor in enumerate(contributors):
        print(f"[{index + 1}] login: {contributor.login}, contributions: {contributor.contributions}")

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_values, arg) for arg in [
                PullRequestRequestMaker(PullRequestQueryMaker.opened_pr(**kwarg)),
                PullRequestRequestMaker(PullRequestQueryMaker.closed_pr(**kwarg)),
                PullRequestRequestMaker(PullRequestQueryMaker.old_pr(**kwarg)),
                IssueRequestMaker(IssueQueryMaker.opened_issue(**kwarg)),
                IssueRequestMaker(IssueQueryMaker.closed_issue(**kwarg)),
                IssueRequestMaker(IssueQueryMaker.old_issue(**kwarg)),
            ]
        ]
    #
    values = [future.result() for future in futures]

    for (task_string, value) in zip([
        "Opened pull request",
        "Closed pull request",
        "Old pull request",
        "Opened issues",
        "Closed issues",
        "Old issues",
    ], values):
        print(f"{task_string}: {value}")


import datetime
if __name__ == '__main__':
    run('fastlane',
        'fastlane',
        'master',
        datetime.date.fromisocalendar(day=1, week=1, year=1995),
        datetime.date.fromisocalendar(day=1, week=1, year=2021),
        )
