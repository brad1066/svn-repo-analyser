from unittest import TestCase, main
from XMLInterpreter import XMLInterpreter
from os.path import exists
from os import remove
import xml.etree.ElementTree as ET

class TestXMLInterpreter(TestCase):

    def setUp(self):

        self.fileName = "TestXML.xml"
        with open(self.fileName, "w") as file:
            self.xml = \
"""<?xml version="1.0" encoding="UTF-8"?>
<log>
    <logentry revision="1">
        <author>user1</author>
        <date>2023-11-14T10:00:00</date>
        <paths>
            <path
                text-mods="true"
                kind="file"
                action="A"
                prop-mods="false">/Sandbox/Oliver/Bank.py</path>
        </paths>
        <msg>Initial commit</msg>
    </logentry>
    <logentry revision="2">
        <author>user2</author>
        <date>2023-11-14T10:00:00</date>
        <paths>
            <path
                text-mods="true"
                kind="file"
                action="A"
                prop-mods="false">/Sandbox/Oliver/Bank.py</path>
        </paths>
        <msg>Initial commit</msg>
    </logentry>
</log>"""
            file.write(self.xml)
        
        self.interpreter = XMLInterpreter(self.fileName)


    def test_initializers(self):

        stringInterpreter = XMLInterpreter(self.fileName)
        treeInterpreter = XMLInterpreter(ET.ElementTree(ET.fromstring(self.xml)))
        # Check that using both variables of the initializer, gets the same output from getDictionary
        self.assertEqual(stringInterpreter.getDictionary(), treeInterpreter.getDictionary())
        # Check that if the class is instantiated with something other than a str or ElementTree, it raises
        # a TypeError
        with self.assertRaises(TypeError):
            integerInterpreter = XMLInterpreter(int(5))
        
    def test_getDictionary(self):
        expectedReturn = {'log': {'logentry': [{'author': 'user1', 'date': '2023-11-14T10:00:00', 'paths': {'path': {'@text-mods': 'true', '@kind': 'file', '@action': 'A', '@prop-mods': 'false', '#text': '/Sandbox/Oliver/Bank.py'}}, 'msg': 'Initial commit', '@revision': '1'}, {'author': 'user2', 'date': '2023-11-14T10:00:00', 'paths': {'path': {'@text-mods': 'true', '@kind': 'file', '@action': 'A', '@prop-mods': 'false', '#text': '/Sandbox/Oliver/Bank.py'}}, 'msg': 'Initial commit', '@revision': '2'}]}}
        
        self.assertEqual(expectedReturn, self.interpreter.getDictionary(self.interpreter.root))

    def tearDown(self):
        # DELETE FILE
        if exists(self.fileName):
            remove(self.fileName)
        return super().tearDown()
    
if __name__ == "__main__":
    main()