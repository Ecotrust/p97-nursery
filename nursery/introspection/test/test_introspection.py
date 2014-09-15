import unittest

from nursery.introspection.introspection import get_class


class testGetClass(unittest.TestCase):

    def testNoDots(self):
        with self.assertRaises(ValueError): 
            get_class('hello')
    
    def testNonExistent(self):
        with self.assertRaises(AttributeError):
            get_class('sys.poodoo')
    
    def testExistent(self):
        cls = get_class('ConfigParser.RawConfigParser')
        import ConfigParser
        
        self.assertEqual(cls, ConfigParser.RawConfigParser, 'Got the wrong class')
    
    