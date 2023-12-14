from unittest import TestCase, main
from Anonymiser import Anonymiser
from CommitLog import CommitLog

class TestAnonymiser(TestCase):

    def setUp(self) -> None:
        
        logs = [{
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
        self.commitLog = CommitLog(logs)
        self.anonmiyser = Anonymiser(self.commitLog)
    
    def test_anonymiseUser(self):
        
        user = "tc12345"
        self.assertNotEqual(self.anonmiyser.anonymiseUser(user), user)
    
    def test_unanonymiseUser(self):

        user = "tc12345"
        userAnonymised = self.anonmiyser.anonymiseUser(user)
        
        self.assertEqual(self.anonmiyser.unanonymiseUser(userAnonymised), user)


if __name__ == "__main__":
    main()