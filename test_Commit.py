from unittest import TestCase, main
from Commit import Commit

class TestCommit(TestCase):
    def setUp(self):
        self.commit1 = Commit(1,
                             author="tc12345",
                             date="2023-11-20T18:20:47.280793Z",
                             paths=[],
                             msg="[Driver: tc12345] [Navigator: tc56789,ab12345] This is a suitably long message for a commit in pair programming")

        self.commit2 = Commit(2,
                            author = "tc56789",
                            date = "2023-11-20T18:50:47.280793Z",
                            paths = [],
                            msg = "[Driver: tc56789] [Navigator: ab12345] This is short")
                            
        
    def test_isPairProgramming(self):
        self.assertEqual(self.commit1.isPairProgramming(), True)
        self.assertEqual(self.commit2.isPairProgramming(), True)

    def test_getDriver(self):
        self.assertEqual(self.commit1.getDriver(), "tc12345")
        self.assertEqual(self.commit2.getDriver(), "tc56789")

    def test_getNavigators(self):
        self.assertEqual(self.commit1.getNavigators(), ["tc56789", "ab12345"])
        self.assertEqual(self.commit2.getNavigators(), ["ab12345"])

    def test_getMessage(self):
        self.assertEqual(self.commit1.getMessage(), "This is a suitably long message for a commit in pair programming")
        self.assertEqual(self.commit2.getMessage(), "This is short")

    def test_msgMatchesRegex(self):
        # Test Driver
        self.assertTrue(self.commit1.msgMatchesRegex(r"\[Driver: tc12345\]"))
        self.assertFalse(self.commit1.msgMatchesRegex(r"\[Driver: tc56789\]"))

        self.assertTrue(self.commit2.msgMatchesRegex(r"\[Driver: tc56789\]"))
        self.assertFalse(self.commit2.msgMatchesRegex(r"\[Driver: tc12345\]"))
        # Test Navigator/s
        self.assertTrue(self.commit1.msgMatchesRegex(r"\[Navigator: tc56789,ab12345\]"))
        self.assertFalse(self.commit1.msgMatchesRegex(r"\[Navigator: tc12345\]"))

        self.assertTrue(self.commit2.msgMatchesRegex(r"\[Navigator: ab12345\]"))
        self.assertFalse(self.commit2.msgMatchesRegex(r"\[Navigator: tc12345\]"))
        
    def test_rateMessageLength(self):
        self.assertEqual(self.commit1.rateMessageLength(), 3)
        self.assertEqual(self.commit2.rateMessageLength(), 1)

        # Forcing 0 expected on message length
        self.commit1.msg = ""
        self.assertEqual(self.commit1.rateMessageLength(), 0)

        # Forcing msg length score of 2
        self.commit2.msg = "_"*150
        self.assertEqual(self.commit2.rateMessageLength(), 1)

        # Forcing 0 expected on message length
        self.commit1.msg = "_"*100
        self.assertEqual(self.commit1.rateMessageLength(), 2)

    def test_setDriverRegex(self):
        self.commit1.setDriverRegex(r"\[Driver:([\sa-zA-Z0-9]+)\]")
        self.assertEqual(self.commit1.driverRegex.pattern, r"\[Driver:([\sa-zA-Z0-9]+)\]")

    def test_setNavigatorsRegex(self):
        self.commit1.setNavigatorsRegex(r"\[Navigator:([\sa-zA-Z0-9]+)\]")
        self.assertEqual(self.commit1.navigatorsRegex.pattern, r"\[Navigator:([\sa-zA-Z0-9]+)\]")

    def test_setMessageLengthBoundaries(self):
        self.commit1.setMessageLengthBoundaries((30, 75, 150))
        self.assertEqual(self.commit1.messageLengthBoundaries, (30, 75, 150))

        self.commit1.setMessageLengthBoundaries((30, 75))
        self.assertEqual(self.commit1.messageLengthBoundaries, (30, 75, 150))

    def test_reprFunction(self):
        self.assertAlmostEqual(self.commit1.__repr__(), "1 -> [Driver: tc12345] [Navigator: tc56789,ab12345] This is a suitably long message for a commit in pair programming")

    def test_getRating(self):
        self.assertEqual(self.commit1.getRating(), 5)
        self.assertEqual(self.commit2.getRating(), 3)
        self.assertNotEqual(self.commit2.getRating(), 2)

    def tearDown(self):
        self.commit1.setDriverRegex(r"\[Driver:([\sa-zA-Z0-9]+)\]")
        self.commit1.setNavigatorsRegex(r"\[Navigator:(([\sa-zA-Z0-9]+[,]?)+)\]")
        return super().tearDown()