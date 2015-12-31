'''
Created on Sep 28, 2015

@author: arnon
'''

import unittest
import sys
import os
from xmlprops import XMLPropsStr
from xmlprops import XMLPropsFile


class TestXMLProps(unittest.TestCase):

    def test_get_match(self):
        try:
            config_file = 'props_unit_test.xml'
            root_loc=os.path.dirname(__file__)
            config_file_name=os.path.join(root_loc,config_file)
            source_file = open(config_file_name,"r")
            props_xml_01 = source_file.read()
            source_file.close()
            xmlprops_str=XMLPropsStr(props=props_xml_01)
            xmlprops_file=XMLPropsFile(props=config_file_name)
        except Exception as e:
            raise Exception('Failed to open and read from file: {}; {}; {}'.format(os.getcwd(),config_file_name, repr(e)))
        
        self.assertEqual(xmlprops_str.get_match(key_prefix='db1.')['password'], 'passworddb')
        self.assertEqual(xmlprops_str.get_match(key_prefix='db1.password')[''], 'passworddb')
        
        self.assertEqual(xmlprops_file.get_match(key_prefix='db1.')['password'], 'passworddb')
        self.assertEqual(xmlprops_file.get_match(key_prefix='db1.password')[''], 'passworddb')
    
    def test_get_order_match(self):
        try:
            config_file = 'props_unit_test.xml'
            root_loc=os.path.dirname(__file__)
            config_file_name=os.path.join(root_loc,config_file)
            source_file = open(config_file_name,"r")
            props_xml_01 = source_file.read()
            source_file.close()
            xmlprops_str=XMLPropsStr(props=props_xml_01)
            xmlprops_file=XMLPropsFile(props=config_file_name)
        except Exception as e:
            raise Exception('Failed to open and read from file: {}; {}; {}'.format(os.getcwd(),config_file_name, repr(e)))
        
        self.assertEqual(xmlprops_str.get_match(key_prefix='db1.')['priority'], '2')
        self.assertEqual(xmlprops_str.get_match(key_prefix='db1.priority')[''], '2')
        
        self.assertEqual(xmlprops_file.get_match(key_prefix='db1.')['priority'], '2')
        self.assertEqual(xmlprops_file.get_match(key_prefix='db1.priority')[''], '2')
    
    def test_get_contain(self):
        try:
            config_file = 'props_unit_test.xml'
            root_loc=os.path.dirname(__file__)
            config_file_name=os.path.join(root_loc,config_file)
            source_file = open(config_file_name,"r")
            props_xml_01 = source_file.read()
            source_file.close()
            xmlprops_str=XMLPropsStr(props=props_xml_01)
            xmlprops_file=XMLPropsFile(props=config_file_name)
        except Exception as e:
            raise Exception('Failed to open and read from file: {}; {}; {}'.format(os.getcwd(),config_file_name, repr(e)))
  
        self.assertEqual(xmlprops_str.get_contain('host'), {'host': 'hw_host', 'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_str.get_contain(key_value='host',exact_match=True), {'host': 'hw_host'})
        self.assertEqual(xmlprops_str.get_contain('db1.host'), {'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_str.get_contain('db.\.port'), {'db2.port': 'portdb2', 'db1.port': 'portdb1'})
        
        self.assertEqual(xmlprops_file.get_contain('host'), {'host': 'hw_host', 'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_file.get_contain(key_value='host',exact_match=True), {'host': 'hw_host'})
        self.assertEqual(xmlprops_file.get_contain('db1.host'), {'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_file.get_contain('db.\.port'), {'db2.port': 'portdb2', 'db1.port': 'portdb1'})
    
    def test_get(self):
        try:
            config_file = 'props_unit_test.xml'
            root_loc=os.path.dirname(__file__)
            config_file_name=os.path.join(root_loc,config_file)
            source_file = open(config_file_name,"r")
            props_xml_01 = source_file.read()
            source_file.close()
            xmlprops_str=XMLPropsStr(props=props_xml_01)
            xmlprops_file=XMLPropsFile(props=config_file_name)
        except Exception as e:
            raise Exception('Failed to open and read from file: {}; {}; {}'.format(os.getcwd(),config_file_name, repr(e)))
  
        self.assertEqual(xmlprops_str.get_contain('host'), {'host': 'hw_host', 'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_str.get_contain(key_value='host',exact_match=True), {'host': 'hw_host'})
        self.assertEqual(xmlprops_str.get_contain('db1.host'), {'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_str.get_contain('db.\.port'), {'db2.port': 'portdb2', 'db1.port': 'portdb1'})
        
        self.assertEqual(xmlprops_file.get_contain('host'), {'host': 'hw_host', 'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_file.get_contain(key_value='host',exact_match=True), {'host': 'hw_host'})
        self.assertEqual(xmlprops_file.get_contain('db1.host'), {'db1.host': 'hostdb'})
        self.assertEqual(xmlprops_file.get_contain('db.\.port'), {'db2.port': 'portdb2', 'db1.port': 'portdb1'})


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestXMLProps))
    unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
