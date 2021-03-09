from utils.jira_rest import JiraRest
from utils.date import Date


class JiraData:
    def __init__(self, server, username, password):
        self._jira_username = username
        self._jira_rest = JiraRest(server, username, password)

    @staticmethod
    def __get_max_lengths(project):
        max_summary_len = 10
        max_comment_len = 10

        for issue in project['issues']:
            if len(project['issues'][issue]['summary']) > max_summary_len:
                max_summary_len = len(project['issues'][issue]['summary'])
            if 'comment' in project['issues'][issue]:
                if len(project['issues'][issue]['summary']) > max_comment_len:
                    max_comment_len = len(project['issues'][issue]['summary'])
        return max_summary_len, max_comment_len

    def get_jira_issues(self, month, year, employee_name):
        search_response = self._jira_rest.search_for_issues_with_individual_worklogs(month, year, employee_name)

        projects = {}
        for issue in search_response['issues']:
            project_name = issue['fields']['project']['name']
            if project_name not in projects.keys():
                projects[project_name] = {}
                projects[project_name]['issues'] = {}

            projects[project_name]['issues'][issue['key']] = {}
            projects[project_name]['issues'][issue['key']]['summary'] = issue['fields']['summary']

            worklogs = self._jira_rest.get_issue_worklogs(issue['key'])
            print('Collecting issue {} data'.format(issue['key']))
            worklog_dates = []
            for worklog in worklogs['worklogs']:
                if 'emailAddress' not in worklog['author']:
                    continue

                if worklog['author']['emailAddress'] == self._jira_username:
                    worklog_date = Date.parse_date(worklog['started'])
                    if worklog_date.month == int(month):
                        worklog_dates.append(worklog_date.day)
                        if 'comment' in worklog:
                            projects[project_name]['issues'][issue['key']]['comment'] = worklog['comment']

            projects[project_name]['issues'][issue['key']]['min_date'] = \
                Date.format_date_with_leading_zeros(min(worklog_dates), month, year)
            projects[project_name]['issues'][issue['key']]['max_date'] = \
                Date.format_date_with_leading_zeros(max(worklog_dates), month, year)

        for project in projects:
            max_summary_len, max_comment_len = self.__get_max_lengths(projects[project])
            projects[project]['max_summary_len'] = max_summary_len
            projects[project]['max_comment_len'] = max_comment_len

        return projects
