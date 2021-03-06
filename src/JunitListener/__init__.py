from .junit_xml import TestSuite, TestCase
import os
import datetime
import tzlocal
import time
import locale
import platform
import pytz


def iso8601(robot_timestring, timezone_str):
    date_time_obj = datetime.datetime.strptime(robot_timestring, '%Y%m%d %H:%M:%S.%f')
    timezone = pytz.timezone(timezone_str)
    timezone_date_time_obj = timezone.localize(date_time_obj)
    return timezone_date_time_obj.isoformat()


class JunitListener(object):
    ROBOT_LISTENER_API_VERSION = 2
    _suites = {}
    _current_case = None
    _current_suite = None
    _testcases = {}

    # suite attributes: name test_cases  hostname id package timestamp properties file log url stdout stderr
    # case attributes: name classname elapsed_sec stdout stderr assertions timestamp status category file line log group url

    def __init__(self, junit_file="junit.xml", junit_xslt="junit-9"):
        self.junit_xslt = junit_xslt
        # self.output=[]
        self.junit_file = junit_file
        language, encoding = locale.getdefaultlocale()
        self.hostname = platform.node()
        self.robot_settings = {}
        self.default_properties = {
            "timezone": tzlocal.get_localzone().zone,
            "timezone_offset": time.timezone,
            "hostname": self.hostname,
            "language": language,
            "encoding": encoding,
        }

    def start_suite(self, name, attrs):
        if len(attrs['tests']) > 0:
            self._current_suite = attrs['longname']
            current_suite = self._current_suite
            attrs['name'] = name
            attrs['libraries'] = set()
            attrs['variables'] = set()
            attrs['resources'] = set()
            attrs['stdout'] = []
            attrs['stderr'] = []
            self._suites[current_suite] = attrs
            self._testcases[current_suite] = {}

    def end_suite(self, name, attrs):
        if len(attrs['tests']) > 0:
            current_suite = attrs['longname']
            attrs['name'] = name
            self._suites[current_suite].update(attrs)
            self._current_suite = None

    def start_test(self, name, attrs):
        current_case = attrs['longname']
        self._current_case = current_case

        attrs['name'] = name
        attrs['stdout'] = []
        attrs['stderr'] = []
        self._testcases[self._current_suite][current_case] = attrs

    def end_test(self, name, attrs):
        current_case = attrs['longname']
        attrs['name'] = name
        self._testcases[self._current_suite][current_case].update(attrs)
        self._current_case = None

    def start_keyword(self, name, attrs):
        pass
        # self.output.append(f"start_keyword: {name} {attrs}")

    def end_keyword(self, name, attrs):
        pass
        # self.output.append(f"end_keyword: {name} {attrs}")

    def log_message(self, message):
        identifiers = ['Return', 'Arguments']
        msg_identifier = message['message'].split(":")[0]
        if msg_identifier not in identifiers:
            if None not in [self._current_case, self._current_suite]:
                if message['level'] == 'FAIL':
                    self._testcases[self._current_suite][self._current_case]['stderr'].append(message['message'])
                else:
                    self._testcases[self._current_suite][self._current_case]['stdout'].append(message['message'])


    def message(self, message):
        if message['message'].startswith("Settings"):
            payload = message['message'].split("\n")[1:]
            for item in payload:
                key, value = item.split(": ")
                try:
                    value = eval(value)
                except NameError:
                    pass
                except SyntaxError:
                    try:
                        value = eval(value.replace("<", "\"<").replace(">", ">\""))
                    except Exception:
                        pass
                except Exception:
                    pass

                self.robot_settings[key] = value

    def library_import(self, name, attrs):
        if self._current_suite:
            self._suites[self._current_suite]['libraries'].add(name)

    def resource_import(self, name, attrs):
        if self._current_suite:
            self._suites[self._current_suite]['resources'].add(attrs['source'])

    def variables_import(self, name, attrs):
        if self._current_suite:
            self._suites[self._current_suite]['variables'].add(attrs['source'])

    def output_file(self, filename):
        self.default_properties['output_file'] = filename

    def log_file(self, filename):
        self.default_properties['log_file'] = filename

    def report_file(self, filename):
        self.default_properties['report_file'] = filename

    def debug_file(self, filename):
        self.default_properties['debug_file'] = filename

    def close(self):
        results = []
        for suite_name, suite_attrs in self._suites.items():
            properties = dict(self.default_properties)
            properties.update(self.robot_settings)
            if suite_attrs['doc']:
                properties['Documentation'] = suite_attrs['doc']

            if suite_attrs['metadata']:
                for key, val in suite_attrs['metadata'].items():
                    properties[key] = val

            for key in ['libraries', 'resources', 'variables']:
                if suite_attrs[key]:
                    properties[key] = ",".join(suite_attrs[key])

            suite = TestSuite(suite_attrs['name'],
                              package=suite_attrs['longname'],
                              id=suite_attrs['id'],
                              timestamp=iso8601(suite_attrs['starttime'], self.default_properties['timezone']),
                              hostname=self.hostname,
                              properties=properties,
                              file=suite_attrs['source'])
            for case, case_attrs in self._testcases[suite_attrs['longname']].items():
                case = TestCase(case_attrs['name'],
                                classname=case_attrs['longname'],
                                elapsed_sec=round(case_attrs['elapsedtime'] / 1000, 3),
                                stdout="\n".join(case_attrs['stdout']),
                                stderr="\n".join(case_attrs['stderr']),
                                )
                if case_attrs['status'] != 'PASS':
                    if case_attrs['critical'] == 'yes':
                        msg = "{}: {}".format(case_attrs['status'], case_attrs['message'])
                        case.add_failure_info(msg)
                    else:
                        msg = "{}: {} - {}".format(case_attrs['status'], case_attrs['message'], 'Skipped due to been marked as non-critical')
                        case.add_skipped_info(msg)

                suite.test_cases.append(case)

            results.append(suite)

        self.junit_file = os.path.join(self.output_path(), self.junit_file)
        print("{:<9}{}".format(self.junit_xslt.capitalize() + ":", self.junit_file))
        with open(self.junit_file, "w") as output:
            TestSuite.to_file(output, results, junit_xslt=self.junit_xslt)
        """
        with open("log.txt","w") as output:
            output.write("\n".join(self.output))
        """

    def output_path(self):
        def guess():
            for name in ['output_file', 'log_file', 'report_file', 'debug_file']:
                temp_file = self.default_properties.get(name, None)
                if temp_file:
                    return os.path.dirname(temp_file)
            return "."
        return self.robot_settings.get('OutputDir', None) or guess()
