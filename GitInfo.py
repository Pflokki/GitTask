import argparse
import datetime
import os

from GitTask.__main__ import run
from GitTask.ResponseError import ParameterError, TokenError

DATE_FORMAT = "YYYY-MM-DD"

HELP = f"""
    This tools provide fetching contributor, issue and pull request info
    
    Available options:
        -t|--token [token] - Access token, using for increase GitHubAPI's rate limit
        -o|--owner [owner] - Owner
        -r|--repo [repo] - Repository name
        -b|--branch [branch] - Branch
        -df|--dfrom [date_from] - Left border for fetch date range, format: {DATE_FORMAT}
        -dt|--dto [date_to] - Right border for fetch date range, format: {DATE_FORMAT}
        
        -h - Show this message
"""


def main():

    parser = argparse.ArgumentParser(description=HELP)

    parser.add_argument("-t", "--token", help="Access token, using for increase GitHubAPI's rate limit")
    parser.add_argument("-o", "--owner", help="Owner", required=True)
    parser.add_argument("-r", "--repo", help="Repository name", required=True)
    parser.add_argument("-b", "--branch", help="Branch", required=True)
    parser.add_argument("-df", "--dfrom", help="Left border for fetch date range, format: {DATE_FORMAT}")
    parser.add_argument("-dt", "--dto", help="Right border for fetch date range, format: {DATE_FORMAT}")

    args = parser.parse_args()

    if args.token:
        os.environ['TOKEN'] = args.token

    owner = args.owner
    repo = args.repo
    branch = args.branch

    try:
        dfrom = datetime.datetime.strptime(args.dfrom, "%Y-%m-%d").date() if args.dfrom else datetime.date(year=1970, day=1, month=1)
        dto = datetime.datetime.strptime(args.dto, "%Y-%m-%d").date() if args.dto else datetime.date.today()
        if dfrom > dto:
            raise ValueError
    except ValueError:
        print("Wrong data format, check help")
        return

    try:
        # time_first = datetime.datetime.now()
        run(owner, repo, branch, dfrom, dto)
        # timedelta = datetime.datetime.now() - time_first
        # print(f"Time spend: {timedelta.total_seconds()}s")  # Time spend: 48.674745
    except ParameterError:
        print("Wrong owner or repository name")
    except TokenError:
        print("Wrong token")


if __name__ == "__main__":
    main()
