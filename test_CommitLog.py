from unittest import TestCase, main
from CommitLog import CommitLog
from Commit import Commit
from copy import deepcopy

class TestCommitLog(TestCase):
    def setUp(self):
        self.logs = [{
            "@revision": 1,
            "author": "tc12345",
            "date": "2023-11-20T18:20:47.280793Z",
            "paths":[],
            "msg": "[Driver: tc12345] [Navigator: tc56789,ab12345] This is a suitably long message for a commit in pair programming"
        },
        {
            "@revision": 2,
            "author": "tc12345",
            "date": "2023-11-20T18:50:47.280793Z",
            "paths":[],
            "msg": "[Driver: tc12345] [Navigator: ab12345] This is short"
        }]

        self.commitLogs = CommitLog(deepcopy(self.logs))
    
    def test_getCommitsFromLogs(self):
        commits = []
        for log in self.logs:
            revision = log["@revision"]
            commits.append(Commit(revision, **log))
        
            
        self.assertListEqual(commits, self.commitLogs.getCommitsFromLogs())
    
    def test_getCommitsByAuthor(self):
        expected = [
            Commit(1, **{
                "@revision": 1,
                "author": "tc12345",
                "date": "2023-11-20T18:20:47.280793Z",
                "paths":[],
                "msg": "[Driver: tc12345] [Navigator: tc56789,ab12345] This is a suitably long message for a commit in pair programming"
            }),
            Commit(2, **{
                "@revision": 2,
                "author": "tc12345",
                "date": "2023-11-20T18:50:47.280793Z",
                "paths":[],
                "msg": "[Driver: tc12345] [Navigator: ab12345] This is short"
            })
        ]
        self.assertListEqual(expected, self.commitLogs.getCommitsByAuthor("tc12345"))
        self.assertNotEqual(expected, self.commitLogs.getCommitsByAuthor("tc23456"))

    def test_getPairProgrammedCommits(self):
        pairProgrammingLogs = deepcopy(self.logs)
        pairProgrammingCommitLogs = CommitLog(pairProgrammingLogs)

        expectedCommits = [commit for commit in pairProgrammingCommitLogs.commits if commit.isPairProgramming()]

        self.assertListEqual(expectedCommits, pairProgrammingCommitLogs.getPairProgrammedCommits(True))

    def test_getCommitRatings(self):
        self.assertDictEqual(self.commitLogs.getCommitRatings(), {"1": 5, "2": 3})
    
    def test_getDriverCommitsByName(self):        
        self.assertDictEqual(self.commitLogs.getDriverCommitsByName(), {'tc12345': [1,2]})
    
    def test_getNavigatorCommitsByName(self):        
        
        self.assertDictEqual(self.commitLogs.getNavigatorCommitsByName(), {'ab12345': [1,2],'tc56789': [1]})

if __name__ == '__main__':
    main()
