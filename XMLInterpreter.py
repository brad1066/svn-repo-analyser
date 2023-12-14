import xml.etree.ElementTree as ET
from collections import defaultdict


class XMLInterpreter():
    def __init__(self, arg: str | ET.ElementTree) -> None:
        if isinstance(arg, str):
            self.filename = arg
            self.tree = ET.parse(self.filename)
            self.root = self.tree.getroot()
        elif isinstance(arg, ET.ElementTree):
            self.filename = None
            self.tree = arg
            self.root = arg.getroot()
        else:
            raise TypeError("Expected a string or xml.etree.ElementTree object")

    def getDictionary(self, tree=None):
        if tree == None:
            tree = self.root
        # Get the tag (title)
        # If the tag has an attribute, create a empty dictionary
        dictionary = {tree.tag: {} if tree.attrib else None}

        # Get a list of children (empty if none)
        children = list(tree)
        # If there are children
        if children:
            # Create a default dictionary to accumulate child elements
            defaultdictionary = defaultdict(list)
            for child in map(self.getDictionary, children):
                for key, value in child.items():
                    defaultdictionary[key].append(value)

            nested_dict = {}
            # Turning the defaultdictionary into a dictionary of dictionaries
            for key, value in defaultdictionary.items():
                if len(value) == 1:
                    nested_dict[key] = value[0]
                else:
                    nested_dict[key] = value
            dictionary = {tree.tag: nested_dict}
    
        # Modifying all attributes so they start with @ symbol
        if tree.attrib:
            dictionary[tree.tag].update(('@' + key, value) for key, value in tree.attrib.items())
        # Modifying all text so that it starts with a #
        if tree.text:
            text = tree.text.strip()
            if children or tree.attrib:
                if text:
                    dictionary[tree.tag]['#text'] = text
            else:
                dictionary[tree.tag] = text

        return dictionary
