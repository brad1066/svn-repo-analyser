from os import walk, path
from utils import *
from XMLInterpreter import XMLInterpreter
import xml.etree.ElementTree as ET
from collections import Counter
from configparser import ConfigParser
from subprocess import call

configs = ConfigParser()
if (path.exists("config.ini")):
    configs.read("config.ini")

class Codebase:
    
    fileEndingConfig = configs.get("FileEndings", "source_code_endings")
    fileEndings = fileEndingConfig.translate(fileEndingConfig.maketrans("", "", "\'[]")).split(", ")

    def __init__(self, pathInRepository):
        self.repositoryRoot = findRootSVN(pathInRepository)
    
    # files filtered through this method
    def filterAllFiles(self,files,filterList = []):
        return filter(lambda file: file not in filterList, files)

    def getAllFiles(self, dir=""):
        files = []

        folderToLookIn = self.repositoryRoot
        if dir != "": folderToLookIn = path.join(self.repositoryRoot, dir)

        for filePath in call(f"svn list -R {folderToLookIn}"):
            files.append(path.join(self.repositoryRoot, filePath))

        return files
    
    def getSourceCodeFiles(self, dir=""):
        if dir != "":
            files = self.getAllFiles(dir)
        else:
            files = self.getAllFiles()

        sourceCodeFiles = []

        for filePath in files:
            if "." in filePath:
                if filePath.split(".")[1] in self.fileEndings:
                    sourceCodeFiles.append(filePath)
        
        return sourceCodeFiles
    
    @staticmethod
    def getFileGrowth(filePath):
        
        # First we need to run "svn log *filePath* --xml"
        # and read the response:
        response, error = runCommand(["svn","log",filePath,"--xml"])
        # Then we can make an ElementTree object for parsing to the XMLInterpreter
        tree = ET.ElementTree(ET.fromstring(response))
        # Create an interpreter, and then interpret the xml to a dictionary
        interpreter = XMLInterpreter(tree)
        xmlDictionary = interpreter.getDictionary()

        # Get a sorted list of revisions 
        listOfRevisions = []
        if isinstance(xmlDictionary["log"]["logentry"], dict):
            listOfRevisions.append(int(xmlDictionary["log"]["logentry"]["@revision"]))
        else:
            for revision in xmlDictionary["log"]["logentry"]:
                listOfRevisions.append(int(revision["@revision"]))

        listOfRevisions = sorted(listOfRevisions)
        
        # Run a command for each revision
        # to check how many lines have been added/removed, and who by
        response, error = runCommand(["svn", "blame", filePath])
        response = response.split("\n")

        revisionDict = {}
    
        for line in response:
            filteredList = list(filter(lambda x: x != "", line.split(" ")))
            if filteredList == []:
                continue

            # If the revision number is already in dictionary
            if filteredList[0] == '-': continue
            if filteredList[0] in revisionDict:
                revisionDict[filteredList[0]].append(filteredList[1])
            else:
                revisionDict[filteredList[0]] = [filteredList[1]]

        # Rather than have a dictionary full of all occurances of someone's name
        # Fill it with the amount of occurances of someone's name, per revision.
        countedRevisionDict = {}
        for key in revisionDict.keys():
            occurances = dict(Counter(revisionDict[key]))
            countedRevisionDict[key] = occurances
        
        return countedRevisionDict
