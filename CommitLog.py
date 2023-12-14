from Commit import Commit

class CommitLog:
    def __init__(self, logs=[]):
        self.logs = logs
        self.commits = self.getCommitsFromLogs()

    def getCommitsFromLogs(self):
        commits = []
        for log in self.logs:
            revision = log['@revision']
            commits.append(Commit(revision, **log))
        
        return commits
    
    def getCommitsByAuthor(self, author):
        return list(filter(lambda commit: commit.author == author, self.commits))
    
    def getCommitsByDriver(self, driver):
        return list(filter(lambda commit: commit.getDriver() == driver, self.commits)) if driver else []
    
    def getCommitsByNavigator(self, navigator):
        return list(filter(lambda commit: navigator in commit.getNavigators() if commit.getNavigators() else False, self.commits))
    
    def getPairProgrammedCommits(self, isPairProgramming=True):
        return list(filter(lambda commit: commit.isPairProgramming() == isPairProgramming, self.commits))
    
    def getCommitRatings(self):
        ratings = {}
        for commit in self.commits:
            ratings[str(commit.revision)] = commit.getRating()
            
        return ratings
    
    def getDriverCommitsByName(self):
        commitDict = {}
        for commit in self.commits:
            driver = commit.getDriver()
            revision = commit.revision
            if driver in commitDict:
                commitDict[driver].append(revision)
            else:
                commitDict[driver] = [revision]
                
        return commitDict
    
    def getNavigatorCommitsByName(self):        
        commitDict = {}
        for commit in self.commits:
            navigators = commit.getNavigators()
            revision = commit.revision
            for navigator in navigators:
                if navigator in commitDict:
                    commitDict[navigator].append(revision)
                else:
                    commitDict[navigator] = [revision]
        return commitDict