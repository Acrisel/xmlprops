'''
Created on Sep 28, 2015

@author: arnon
'''

import unittest
import sys
import os
from xmlprops import XMLPropsStr
from xmlprops import XMLPropsFile

props_xml_01='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>

<comment>
  This properties file provides MySql configuration 
  definitions for Tax tables DB
</comment>

<comment>Provide the type of DB this properties for</comment>
<entry key="product">MySql</entry>

<comment>Pool Level Defaults</comment>
<entry key="service_mode">BF</entry>
<entry key="exposure">shared</entry>
<entry key="makers">db1</entry>

<comment>Resource Making Defaults</comment>
<entry key="max_active">10</entry>
<entry key="init_active">1</entry>

<comment>Resource Information</comment>
<entry key="db1.user">userdb</entry>
<entry key="db1.password">passworddb</entry>
<entry key="db1.host">hostdb</entry>
<entry key="db1.port">portdb</entry>
<entry key="db1.database">databasedb</entry>
<entry key="db1.use_unicode">True</entry>
<entry key="db1.charset">utf8</entry>
<entry key="db1.priority">1</entry>
<entry key="db1.priority">2</entry>

</properties>
'''

class TestXMLProps(unittest.TestCase):

    def test_get_match_str(self):
        xmlprops=XMLPropsStr(props=props_xml_01)
        
        self.assertEqual(xmlprops.get_match(key_prefix='db1.')['password'], 'passworddb')
        self.assertEqual(xmlprops.get_match(key_prefix='db1.password')[''], 'passworddb')
    
    def test_get_order_match_str(self):
        xmlprops=XMLPropsStr(props=props_xml_01)
        
        self.assertEqual(xmlprops.get_match(key_prefix='db1.')['priority'], '2')
        self.assertEqual(xmlprops.get_match(key_prefix='db1.priority')[''], '2')
    
    def test_get_match_file(self):
        """ 
        Write configuration definition to file and unit-test XMLPropsFile
        This is to keep consistency with unit-tests for XMLPropsStr
        """
        config_file_name = "props_unit_test.xml"
        try:
            target_file = open(config_file_name,"w")
            target_file.write(props_xml_01)
            target_file.close()
        except Exception as e:
                raise Exception('Failed to create and write to file: {}; {}; {}'.format(os.getcwd(),config_file_name, repr(e)))

        xmlprops=XMLPropsFile(props=config_file_name)
        os.remove(config_file_name)
        
        self.assertEqual(xmlprops.get_match(key_prefix='db1.')['password'], 'passworddb')
        self.assertEqual(xmlprops.get_match(key_prefix='db1.password')[''], 'passworddb')
        
    def test_get_order_match_file(self):
        """ 
        Write configuration definition to file and unit-test XMLPropsFile
        This is to keep consistency with unit-tests for XMLPropsStr
        """
        config_file_name = "props_unit_test.xml"
        try:
            target_file = open(config_file_name,"w")
            target_file.write(props_xml_01)
            target_file.close()
        except Exception as e:
                raise Exception('Failed to create and write to file: {}; {}; {}'.format(os.getcwd(),config_file_name, repr(e)))

        xmlprops=XMLPropsFile(props=config_file_name)
        os.remove(config_file_name)
        
        self.assertEqual(xmlprops.get_match(key_prefix='db1.')['priority'], '2')
        self.assertEqual(xmlprops.get_match(key_prefix='db1.priority')[''], '2')


if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestXMLProps))
    unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)