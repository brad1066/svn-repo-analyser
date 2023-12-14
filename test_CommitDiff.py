# test_CommitDiff.py
import unittest
from Commit import Commit
from CommitDiff import CommitDiff

class TestCommitDiff(unittest.TestCase):
    def setUp(self):
        # Create sample commit objects for testing
        old_commit = Commit(revision="1", paths=["file1.txt", "file2.txt"], msg="Commit 1")
        new_commit = Commit(revision="2", paths=["file2.txt", "file3.txt"], msg="Commit 2")
        self.commit_diff = CommitDiff(old_commit, new_commit)

    def test_get_changes(self):
        changes = self.commit_diff.get_changes()

        self.assertEqual(changes["added"], ["file3.txt"])
        self.assertEqual(changes["deleted"], ["file1.txt"])
        self.assertEqual(changes["modified"], ["file2.txt"])


if __name__ == '__main__':
    unittest.main()