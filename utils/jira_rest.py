from requests import get
from utils.date import Date


class JiraRest(object):

    def __init__(self, server, user, password):
        self._server = server
        self._user = user
        self._password = password

    def search_for_issues_with_individual_worklogs(self, month, year, employee):
        from_date, to_date = Date.get_month_range(month, year)
        params = {
            'fields': 'key,summary,project',
            'jql': 'worklogAuthor={0} AND worklogDate>={1} AND worklogDate<={2}'.format(employee, from_date, to_date)
        }
        url = "{}{}".format(self._server, '/rest/api/2/search')
        response = get(url, params=params, auth=(self._user, self._password))
        return response.json()

    def get_issue_worklogs(self, issue_id):
        url = "{}{}".format(self._server, '/rest/api/2/issue/{}/worklog'.format(issue_id))
        response = get(url, auth=(self._user, self._password))
        return response.json()
