import unittest

from find_level import *

class TestFindLevel (unittest.TestCase):
    levels_file = "data/eggnogv4.levels.txt"

    def test_parse_levels_file(self):
        levels = parse_levels_file(self.levels_file)
        self.assertTrue(levels)
        with self.assertRaises(IOError):
            parse_levels_file("file_does_not_exist")

    def test_smallest_group(self):
        levels = parse_levels_file(self.levels_file)
        self.assertEqual(smallest_group([240176, 486041, 578458], levels), 5338)
        # TODO add some negative test cases here

    def test_find_human_in_mammals(self):
        levels = parse_levels_file(self.levels_file)
        query_org = 9606 # human
        search_level = 40674 # mammals
        search_orgs = []
        self.assertEqual(
            smallest_group(get_members(search_level, levels), levels), search_level)
        self.assertEqual(
            find_level(query_org, search_level, search_orgs, self.levels_file), search_level)

    # TODO add a version of test_find_human_in_mammals that uses search_orgs instead of the level

    # TODO what other tests should be added?

suite = unittest.TestLoader().loadTestsFromTestCase(TestFindLevel)
unittest.TextTestRunner(verbosity=2).run(suite)
