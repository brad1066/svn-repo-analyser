from unittest import TestCase, main
from utils import *

class TestXMLInterpreter(TestCase):

    def test_runCommand(self):
        expectedReturn = "Sandbox/\r\nbranches/\r\ntags/\r\ntrunk/\r\n"
        returned, error = runCommand(["svn", "list"])
        self.assertEqual(returned, expectedReturn)
        self.assertEqual(error, "")


if __name__ == "__main__":
    main()