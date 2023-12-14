from os import getcwd, path
from unittest import TestCase, main
from Codebase import Codebase

# I haven't written a test case for getAllFiles as it's very cumbersome, includes all sandbox and other files, and we would
# need to re-code it every time any file/folder would be added to the repo.
class test_Codebase(TestCase):

    GIVEN_PATH = ""

    def setUp(self):
        self.codebase = Codebase(self.GIVEN_PATH)
        self.trunkPath = path.join(self.codebase.repositoryRoot, "trunk")

    def test_getSourceCodeFiles(self):
        # This test will fail as soon as another file (ending in .py) is added to the trunk directory
        sourceCodeFiles = sorted(self.codebase.getSourceCodeFiles("trunk"))
        
        expected = [path.join(self.trunkPath, "Anonymiser.py"),
                    path.join(self.trunkPath, "Codebase.py"),
                    path.join(self.trunkPath, "Commit.py"),
                    path.join(self.trunkPath, "CommitDiff.py"),
                    path.join(self.trunkPath, "CommitLog.py"),
                    path.join(self.trunkPath, "Statistics.py"),
                    path.join(self.trunkPath, "XMLInterpreter.py"),
                    path.join(self.trunkPath, "main.pyw"),
                    path.join(self.trunkPath, "test_Anonymiser.py"),
                    path.join(self.trunkPath, "test_Codebase.py"),
                    path.join(self.trunkPath, "test_Commit.py"),
                    path.join(self.trunkPath, "test_CommitDiff.py"),
                    path.join(self.trunkPath, "test_CommitLog.py"),
                    path.join(self.trunkPath, "test_XMLInterpreter.py"),
                    path.join(self.trunkPath, "test_utils.py"),
                    path.join(self.trunkPath, "utils.py")]
        

        for i, sourceCodeFile in enumerate(sourceCodeFiles):
            self.assertEqual(expected[i], sourceCodeFile)

    def test_getFileGrowth(self):
        # This test will fail when CommitLog is updated.
        expectedValue = {'50': {'bb20066': 12}, '36': {'bb20066': 1}, '56': {'bb20066': 3}, '59': {'bl20643': 2}, '60': {'bl20643': 1}, '64': {'bb20066': 1}, '70': {'bb20066': 5}, '76': {'bb20066': 1}, '72': {'lc21948': 6}, '73': {'bb20066': 7}, '74': {'lc21948': 6}, '75': {'lc21948': 6}}
        codeGrowth = self.codebase.getFileGrowth(path.join(self.trunkPath, "CommitLog.py"))
        self.assertEqual(expectedValue, codeGrowth)

    

if __name__ == "__main__":
    #Assuming you're only going to run this file from within the Project folder
    test_Codebase.GIVEN_PATH = getcwd()
    main()
    