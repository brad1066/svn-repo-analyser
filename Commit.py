import re
import math
from configparser import ConfigParser
from utils import findRootSVN
from os import getcwd, path

configs = ConfigParser()
if (path.exists("config.ini")):
    configs.read("config.ini")

class Commit:
    # Static Fields
    driverRegex = re.compile(configs.get("RegexPatterns", "driver") or r"\[Driver:([\sa-zA-Z0-9]+)\]")
    navigatorsRegex = re.compile(configs.get("RegexPatterns", "navigators") or r"\[Navigator:(([\sa-zA-Z0-9]+[,]?)+)\]")
    messageLengthBoundaries = (50, 100, 150)
    if (lowerBound := configs.get("RatingParameters", "lower_msg_length_boundary"))\
        and (middleBound := configs.get("RatingParameters", "medium_msg_length_boundary")) \
        and (upperBound := configs.get("RatingParameters", "upper_msg_length_boundary")):
        try: messageLengthBoundaries = (int(lowerBound), int(middleBound), int(upperBound))
        except: pass
    
    def __init__(self, revision, **kwargs):
        """
        Used to represent a logentry xml node
        """
        self.revision = revision
        self.author = kwargs.get("author", "")
        self.date = kwargs.get("date", "")
        self.paths = kwargs.get("paths", [])
        self.msg = kwargs.get("msg", "")
        self.revprops = kwargs.get("revprops", [])
        self.reverseMerge = kwargs.get("reverse-merge", []) 
        self.participants = [self.author]
        
        if self.msg == None: self.msg = ""

        driver = self.getDriver()
        if driver != False and driver not in self.participants:
            self.participants.append(driver)
        navigators = self.getNavigators()
        if navigators != False:
            for navigator in navigators:
                if navigator not in self.participants:
                    self.participants.append(navigator)

    def isPairProgramming(self):
        """Gets if the commit uses pair programming"""
        return bool(self.driverRegex.findall(self.msg) and self.navigatorsRegex.findall(self.msg))
    
    def getDriver(self):
        """Gets the driver (single) if there is one, of False otherwise"""
        matches = self.driverRegex.findall(self.msg)
        if len(matches) <= 0: return None

        return matches[0].strip()
        
    def getNavigators(self):
        """Gets the navigators (list) if there are any, of False otherwise"""
        matches = self.navigatorsRegex.findall(self.msg)
        if len(matches) <= 0: return []
        matches = matches[0]

        navigators = []

        for navigator in matches[0].split(','):
            navigators.append(navigator.strip(' '))
        return navigators

    def getMessage(self):
        message = self.msg
        message = self.driverRegex.sub('', self.msg).strip()
        message = self.navigatorsRegex.sub('', message).strip()
        return message
    
    
    def msgMatchesRegex(self, regex, flags=0):
        matches = re.findall(regex, self.msg, flags=flags)
        return len(matches) > 0
    
    def rateMessageLength(self):
        # Retrieve message body
        messageLength = len(self.getMessage())

        if messageLength == 0:
            # There is no message
            return 0
        if messageLength < self.messageLengthBoundaries[0]:
            # This is not sufficient
            return 1
        if messageLength < self.messageLengthBoundaries[1]:
            # This is good
            return 3
        if messageLength < self.messageLengthBoundaries[2]:
            # This is getting too long
            return 2
        
        # Otherwise we know it's way too long.
        return 1
    
    def getRating(self):
        messageLengthRating = self.rateMessageLength()
        hasDriverRating = [0, 1][self.getDriver() != False]
        hasNavigatorsRating = [0, 1][self.getNavigators() != False and self.getNavigators() != []]
        return messageLengthRating + hasDriverRating + hasNavigatorsRating


    @staticmethod
    def setDriverRegex(regex):
        """Sets the static regex used to find the driver"""
        Commit.driverRegex = re.compile(regex)
        configs.set('RegexPatterns', 'driver', regex)
        with open('config.ini', 'w') as file:
            configs.write(file)            
    
    @staticmethod
    def setNavigatorsRegex(regex):
        """Sets the static regex used to find the navigators"""
        Commit.navigatorsRegex = re.compile(regex)
        configs.set('RegexPatterns', 'navigators', regex)
        with open('config.ini', 'w') as file:
            configs.write(file)               

    @staticmethod
    def setMessageLengthBoundaries(boundaries):
        """Sets the static boundaries used to report the quality of commit message."""
        if len(boundaries) != 3:
            return False
        Commit.messageLengthBoundaries = boundaries
        configs.set('RatingParameters', 'lower_msg_length_boundary', str(boundaries[0]))
        configs.set('RatingParameters', 'medium_msg_length_boundary', str(boundaries[1]))
        configs.set('RatingParameters', 'upper_msg_length_boundary', str(boundaries[2]))
        return True

    def __eq__(self, other):
        if not isinstance(other, Commit): return False
        return self.revision == other.revision \
                and self.author == other.author \
                and self.date == other.date \
                and self.paths == other.paths \
                and self.msg == other.msg \
                and self.revprops == other.revprops \
                and self.reverseMerge == other.reverseMerge

    def __repr__(self):
        return f"{self.revision} -> {self.msg}"
