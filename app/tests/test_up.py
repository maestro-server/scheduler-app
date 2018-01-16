
import unittest

class BasicTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    def test_main_page(self):
        self.assertEqual(200, 200)


if __name__ == "__main__":
    unittest.main()