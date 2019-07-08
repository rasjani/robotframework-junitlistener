import robot
import unittest
import os
import xmlschema
from tempfile import TemporaryDirectory
from xmlrunner import XMLTestRunner
import sys

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CURRENT_DIRECTORY,"..","src"))
from JunitListener import JunitListener



class JunitListenerAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.vendor_directory = os.path.join(CURRENT_DIRECTORY,"..", "vendor")
        self.temp_dir = TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_schema_8(self):
        schema_version = 8
        schema_file = os.path.join(self.vendor_directory, f"junit-{schema_version}.xsd")
        schema = xmlschema.XMLSchema(schema_file)
        result_file = os.path.join(self.temp_dir.name,"results.xml")
        robot.run("test",
                  listener=JunitListener(result_file, schema_version),
                  critical="working",
                  noncritical="notworking",
                  console="none",
                  log="NONE",
                  report="NONE",
                  output="NONE",
                  loglevel="NONE")
        schema.validate(result_file)

    def test_schema_9(self):
        schema_version = 9
        schema_file = os.path.join(self.vendor_directory, f"junit-{schema_version}.xsd")
        schema = xmlschema.XMLSchema(schema_file)
        result_file = os.path.join(self.temp_dir.name,"results.xml")
        robot.run("test",
                  listener=JunitListener(result_file, schema_version),
                  critical="working",
                  noncritical="notworking",
                  console="none",
                  log="NONE",
                  report="NONE",
                  output="NONE",
                  loglevel="NONE")
        schema.validate(result_file)

    def test_schema_10(self):
        schema_version = 10
        schema_file = os.path.join(self.vendor_directory, f"junit-{schema_version}.xsd")
        schema = xmlschema.XMLSchema(schema_file)
        result_file = os.path.join(self.temp_dir.name,"results.xml")
        robot.run("test",
                  listener=JunitListener(result_file, schema_version),
                  critical="working",
                  noncritical="notworking",
                  stdout="NONE",
                  console="none",
                  log="NONE",
                  report="NONE",
                  output="NONE",
                  loglevel="NONE")
        schema.validate(result_file)


if __name__ == '__main__':
    with open('acceptance_tests.xml', 'wb') as output:
        unittest.main(
            testRunner=XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
    unittest.main()

