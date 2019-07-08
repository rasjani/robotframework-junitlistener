from .junit_xml import TestSuite, TestCase
import tzlocal
import time
import locale
import platform


class JunitListener(object):
    ROBOT_LISTENER_API_VERSION = 2
    _suites = {}
    _current_case = None
    _current_suite = None
    _testcases = {}

    # suite attributes: name test_cases  hostname id package timestamp properties file log url stdout stderr
    # case attributes: name classname elapsed_sec stdout stderr assertions timestamp status category file line log group url

    def __init__(self, junit_file="junit.xml", schema_version=9):
        self.schema_version = int(schema_version)
        # self.output=[]
        self.junit_file = junit_file
        language, encoding = locale.getdefaultlocale()
        self.hostname = platform.node()
        self.default_properties = {
            "timezone": tzlocal.get_localzone().zone,
            "timezone_offset": time.strftime('%Z%z'),
            "hostname": self.hostname,
            "language": language,
            "encoding": encoding,
        }

    def start_suite(self, name, attrs):
        if len(attrs['tests']) > 0:
            self._current_suite = attrs['longname']
            current_suite = self._current_suite
            attrs['name'] = name
            self._suites[current_suite] = attrs
            self._testcases[current_suite] = {}
            # self.output.append(f"start_suite: {name} {attrs}")

    def end_suite(self, name, attrs):
        if len(attrs['tests']) > 0:
            current_suite = attrs['longname']
            attrs['name'] = name
            self._suites[current_suite].update(attrs)

    def start_test(self, name, attrs):
        current_case = attrs['longname']
        self._current_case = current_case

        attrs['name'] = name
        self._testcases[self._current_suite][current_case] = attrs

    def end_test(self, name, attrs):
        current_case = attrs['longname']
        attrs['name'] = name
        self._testcases[self._current_suite][current_case].update(attrs)

    def start_keyword(self, name, attrs):
        pass
        # self.output.append(f"start_keyword: {name} {attrs}")

    def end_keyword(self, name, attrs):
        pass
        # self.output.append(f"end_keyword: {name} {attrs}")

    def log_message(self, message):
        pass
        # self.output.append(f"log_message: {message}")

    def library_import(self, name, attrs):
        pass
        # self.output.append(f"library_import: {name} {attrs}")

    def resource_import(self, name, attrs):
        pass
        # self.output.append(f"resource_import: {name} {attrs}")

    def variables_import(self, name, attrs):
        pass
        # self.output.append(f"variables_import: {name} {attrs}")

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
            if suite_attrs['doc']:
                properties['Documentation'] = suite_attrs['doc']

            if suite_attrs['metadata']:
                for key, val in suite_attrs['metadata'].items():
                    properties[key] = val

            suite = TestSuite(suite_attrs['name'],
                              package=suite_attrs['longname'],
                              id=suite_attrs['id'],
                              timestamp=suite_attrs['starttime'],
                              hostname=self.hostname,
                              properties=properties,
                              file=suite_attrs['source'],
                              schema_version=self.schema_version)
            for case, case_attrs in self._testcases[suite_attrs['longname']].items():
                case = TestCase(case_attrs['name'],
                                classname=case_attrs['longname'],
                                elapsed_sec=case_attrs['elapsedtime'] / 1000,
                                schema_version=self.schema_version,
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
        """
        with open("log.txt","w") as output:
            output.write("\n".join(self.output))
        """
        with open(self.junit_file, "w") as output:
            TestSuite.to_file(output, results, schema_version=self.schema_version)
