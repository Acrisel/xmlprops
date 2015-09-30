'''
Created on Sep 28, 2015

@author: arnon
'''

import unittest
from xmlprops import XMLPropsStr as XMLProps

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

</properties>
'''

class TestXMLProps(unittest.TestCase):

    def test_get_fix(self):
        xmlprops=XMLProps(props=props_xml_01)
        self.assertEqual(xmlprops.get_by_fix(key_prefix='db1.')['password'], 'passworddb')


if __name__ == '__main__':
    unittest.main()