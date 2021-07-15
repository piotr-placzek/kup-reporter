import argparse
from config.default import Config
from jira_data import JiraData
from report import Report
from pathlib import Path


class Main:
    def __init__(self, server, username, password):
        self._username = username
        self._jira_data = JiraData(server, username, password)
        self._report = Report()
        self._report_name_template = '{}.{}.xlsx'

    def generate(self, month, year, reports_location):
        print('Generation start.')
        employee_name = self._username
        projects = self._jira_data.get_jira_issues(month, year, employee_name)
        report_name = self._report_name_template.format(month, year)

        Path(reports_location).mkdir(parents=True, exist_ok=True)
        report_location = '{}/{}'.format(reports_location, report_name)
        self._report.generate_report(projects, report_location)
        print('Generation end in location {}.'.format(report_location))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--server', default=Config.Jira.SERVER, help='Overwrite default JIRA server.')
    PARSER.add_argument('-u', '--username', default=Config.Jira.USERNAME, help='Overwrite default JIRA username.')
    PARSER.add_argument('-p', '--password', default=Config.Jira.PASSWORD, help='Overwrite default JIRA password.')
    PARSER.add_argument('-y', '--year', default=Config.Report.YEAR, help='Overwrite default report year.')
    PARSER.add_argument('-m', '--month', default=Config.Report.MONTH, help='Overwrite default report month.')
    PARSER.add_argument('-r', '--reports_location', default=Config.Report.REPORTS_LOCATION,
                        help='Overwrite default reports location.')

    args = PARSER.parse_args()
    report = Main(args.server, args.username, args.password)
    report.generate(args.month, args.year, args.reports_location)
