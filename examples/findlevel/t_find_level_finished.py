import unittest

import os, sys
lib_path = os.path.abspath('../backend')
sys.path.append(lib_path)

from find_level import *

class TestFindLevel (unittest.TestCase):
    levels_file = "data/eggnogv4.levels.txt"
    levels_file_mammals = "data/eggnog.mammals"
    
    def test_smallest_group(self):
        levels = parse_levels_file(self.levels_file)
        self.assertEqual( smallest_group([240176, 486041, 578458], levels) , 5338)


    def test_parse_levels_file(self):
        levels = parse_levels_file(self.levels_file)
        with self.assertRaises(IOError):
            parse_levels_file("file_does_not_exist")
        self.assertTrue(levels, 'Levels file opened and read')
        self.assertEqual(get_size(6231, levels), 7)
        self.assertEqual(get_name(40674, levels), "Mammals")
        self.assertEqual(get_members(5338, levels), [240176, 486041, 578458])

    def test_get_members(self):
        levels = parse_levels_file(self.levels_file)
        self.assertTrue(get_members(40674, levels))
        self.assertEquals(get_members(40674, levels), [9258, 9305, 9315, 9361, 9371, 9478, 9483, 9544, 9593, 9598, 9601, 9606, 9615, 9646, 9669, 9685, 9739, 9785, 9796, 9813, 9823, 9913, 9986, 10020, 10090, 10116, 10141, 13616, 30608, 30611, 37347, 43179, 59463, 61853, 132908])
        self.assertTrue(get_members('40674', levels))
        self.assertRaises(KeyError, get_members, -1, levels)

    def test_find_human_in_mammals(self):
        levels = parse_levels_file(self.levels_file)
        query_org = 9606 # human
        search_level = 40674 # mammals
        search_orgs = []
        self.assertEqual(smallest_group(get_members(search_level, levels), levels), search_level)
        self.assertEqual(find_level(query_org, search_level, search_orgs, self.levels_file), search_level)

        search_orgs = None
        self.assertEqual(smallest_group(get_members(search_level, levels), levels), search_level)
        self.assertEqual(find_level(query_org, search_level, search_orgs, self.levels_file), search_level)

    def test_find_level_exceptions(self):
        levels = parse_levels_file(self.levels_file)
        query_org = 9606 # human

        # neither specified
        search_level = '' 
        search_orgs = ''
        self.assertRaises(Exception, find_level, query_org, search_level, search_orgs, self.levels_file)

        search_level = None
        search_orgs = None
        self.assertRaises(Exception, find_level, query_org, search_level, search_orgs, self.levels_file)

        # invalid orthologous group taxid
        search_level = -1
        search_orgs = []
        self.assertRaises(Exception, find_level, query_org, search_level, search_orgs, self.levels_file)


    def test_find_fly_in_mammals(self):
        levels = parse_levels_file(self.levels_file)
        query_org = 7227 # fly
        search_level = 40674 # mammals
        search_orgs = []
        self.assertEqual(smallest_group(get_members(search_level, levels) + [query_org], levels), 33213)
        self.assertEqual(find_level(query_org, search_level, search_orgs, self.levels_file), 33213) # Bilateria

    def test_cannot_find(self):
        # test that if we try to find an organism that does not exist in levels, then we will throw an exception
        levels = parse_levels_file(self.levels_file_mammals)
        query_org = 7227 # fly
        search_level = 40674 # mammals
        search_orgs = []
        self.assertRaises(Exception, smallest_group, get_members(search_level, levels).append(query_org), levels)

    def test_find_human_in_mammals_by_orgs(self):
        levels = parse_levels_file(self.levels_file)
        query_org = 9606 # human
        search_level = ''
        search_orgs = [9258, 61853] # platypus, gibbon
        self.assertEqual(smallest_group(search_orgs + [query_org], levels), 40674)
        self.assertEqual(find_level(query_org, search_level, search_orgs, self.levels_file), 40674)
        
        search_level = None
        self.assertEqual(smallest_group(search_orgs + [query_org], levels), 40674)
        self.assertEqual(find_level(query_org, search_level, search_orgs, self.levels_file), 40674)

        search_level = 40674 # mammals
        self.assertEqual(smallest_group(search_orgs + [query_org], levels), 40674)
        self.assertEqual(find_level(query_org, search_level, search_orgs, self.levels_file), 40674)


suite = unittest.TestLoader().loadTestsFromTestCase(TestFindLevel)
unittest.TextTestRunner(verbosity=2).run(suite)
