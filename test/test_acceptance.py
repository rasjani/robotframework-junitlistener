import robot
import unittest
import os
import xmlschema
from tempfile import TemporaryDirectory
from xmlrunner import XMLTestRunner
import sys

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
VENDOR_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "..", "src", "JunitListener", "vendor")
sys.path.append(os.path.join(CURRENT_DIRECTORY, "..", "src"))
from JunitListener import JunitListener  # noqa: E402


def test_template(schema_base, temp_dir):
    schema_file = os.path.join(VENDOR_DIRECTORY, f"{schema_base}.xsd")
    schema = xmlschema.XMLSchema(schema_file)
    result_file = os.path.join(temp_dir, "results.xml")
    robot.run("test",
              listener=JunitListener(result_file, schema_base),
              critical="working",
              noncritical="notworking",
              console="none",
              log="NONE",
              report="NONE",
              output="NONE",
              loglevel="NONE")
    schema.validate(result_file)


class JunitListenerAcceptanceTests(unittest.TestCase):

    def setUp(self):
        self.vendor_directory = os.path.join(CURRENT_DIRECTORY, "..", "vendor")
        self.temp_dir = TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_schema_8(self):
        schema_version = 8
        schema_base = f"junit-{schema_version}"
        test_template(schema_base, self.temp_dir.name)

    def test_schema_9(self):
        schema_version = 9
        schema_base = f"junit-{schema_version}"
        test_template(schema_base, self.temp_dir.name)

    def test_schema_10(self):
        schema_version = 10
        schema_base = f"junit-{schema_version}"
        test_template(schema_base, self.temp_dir.name)

    def test_schema_JUnit(self):
        schema_base = "JUnit"
        test_template(schema_base, self.temp_dir.name)

    def test_schema_xunit(self):
        schema_base = "xunit"
        test_template(schema_base, self.temp_dir.name)


if __name__ == '__main__':
    with open('acceptance_tests.xml', 'wb') as output:
        unittest.main(testRunner=XMLTestRunner(output=output),
                      failfast=False, buffer=False, catchbreak=False)
