from utils.jira_rest import JiraRest
from utils.date import Date


class JiraData:
    def __init__(self, server, username, password):
        self._jira_username = username
        self._jira_rest = JiraRest(server, username, password)

    def get_jira_issues(self, month, year, employee_name):
        search_response = self._jira_rest.search_for_issues_with_individual_worklogs(month, year, employee_name)

        issues = {}
        max_summary_len = 10
        max_comment_len = 10
        for issue in search_response['issues']:
            issues[issue['key']] = {}
            issues[issue['key']]['summary'] = issue['fields']['summary']

            if len(issue['fields']['summary']) > max_summary_len:
                max_summary_len = len(issue['fields']['summary'])

            worklogs = self._jira_rest.get_issue_worklogs(issue['key'])
            print('Collecting issue {} data'.format(issue['key']))
            worklog_dates = []
            for worklog in worklogs['worklogs']:
                if worklog['author']['emailAddress'] == self._jira_username:
                    worklog_date = Date.parse_date(worklog['started'])
                    if worklog_date.month == month:
                        worklog_dates.append(worklog_date.day)
                        if 'comment' in worklog:
                            issues[issue['key']]['comment'] = worklog['comment']
                            if len(worklog['comment']) > max_comment_len:
                                max_comment_len = len(worklog['comment'])

            issues[issue['key']]['min_date'] = \
                Date.format_date_with_leading_zeros(min(worklog_dates), month, year)
            issues[issue['key']]['max_date'] = \
                Date.format_date_with_leading_zeros(max(worklog_dates), month, year)

        return issues, max_summary_len, max_comment_len
