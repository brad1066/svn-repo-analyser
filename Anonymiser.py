from CommitLog import CommitLog
import random

class Anonymiser:

    def __init__(self, commitLog: CommitLog):
        participantList = []

        for commit in commitLog.commits:
            for participant in commit.participants:
                if participant not in participantList and participant != None:
                    participantList.append(participant)

        random.shuffle(participantList)

        self.anonymisedMap = {}
        for participant in participantList:
            self.anonymisedMap[participant] = "User " + str(participantList.index(participant) + 1)


    def anonymiseUser(self, userName):
        return self.anonymisedMap[userName]
    
    def unanonymiseUser(self, anonymisedName):
        for userName, anonymisedUserName in self.anonymisedMap.items():
            if anonymisedName == anonymisedUserName:
                return userName
        return False
    
    def getAnonymisedUsers(self):
        anonymisedUsers = []
        for user in self.anonymisedMap.keys():
            anonymisedUsers.append(self.anonymiseUser(user))
        return anonymisedUsers

    def getUsers(self):
        users = []
        for user in self.anonymisedMap.keys():
            users.append(user)
        return users