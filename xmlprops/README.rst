xmlprops provides mechanism for to access and manipulate XML based properties.

Overview
========
XMLProps provides means to access properties that are stored in XML (file or string) - Java XML style.  

There are two main classes xmlprops provides:
  1. XMLPropsFile: file based XML that containing properties
  2. XMLPropsStr: string base XML that containing properties

Both classes inherit from *dict* class.
Both classes provide similar methods to allow stractured access to the properties.    

Both classes inherit same base  class that provides access and manipulation 
methods that used by XMLProps family.  

A property is represented by key value XML entries.
    
Key: property path.  string names separated by, usually, '.' (dot). Key examples:
  1. 'factory_name'
  2. 'arizona.capitol'
  3. 'texas.dallas.mayor'
             
The property name is the last element in property path (similar to basename in path methods)
The property hierarchy is the path to it.
Value: property value.  string representing the value assignment to property
    
The get dict function '[]' was enhanced to include hierarchical get.
On the item a.b.c; get will try to get c, a.c, and a.b.c.
The last one available, wins.

Functions
=========
get(key, key_sep=None)
----------------------
Similar to **get()** "dict" function '[]' but in addition adds hierarchical relations.
**get()** looks for the *key* in it loaded properties.  

Assuming key is property path, the following order of search will be done (key is 'a.b.c.'):
  1. First lookup c, 
  2. Then lookup 'a.c' 
  3. And lastly look for 'a.b.c.'

The last found match wins.
     
set(key, value)
---------------
Sets dictionary *key* with *value*

get_keys(prefix, keys, key_sep=None)
------------------------------------
Return a dictionary for *prefix* and list of *keys*

get_match(key_prefix=None, key_suffix=None, key_sep=None, value_sep = None, decrypt=False)
------------------------------------------------------------------------------------------
Returns *OrderedDict* with all keys matching the criteria.
Look for *key* for *key_prefix* and *key_suffix* 
Each found key is loaded into a dictionary
The *key* in the returned dictionary is stripped of its prefix.
The function returns newly created dictionary
If you want the prefix to end with '.' delimiter; use 'prefix.' as key_prefix.
If *value_sep* is provided, it is used to separate the value of the element into a list.
If *decrypt*, encrypted fields with ending with _encrypted will be decrypted

get_re(key_re=None, value_sep = None, decrypt=False)
----------------------------------------------------
The function looks for a keys that fits regular expression.
**key_re** is string of a Pythonic regular expression        
If value_sep provided, it is used to separate the value of the element into a list.
Returns *dict* object.        

get_contain(key_value=None, ignore_case=False, exact_match=False, value_sep = None, decrypt=False)
--------------------------------------------------------------------------------------------------
The function looks for a keys that that has **key_value** in them.

Parameters:
  1. *key_value*: exact match of *key* or Pythonic regular expression 
  1. *ignore_case*: if set will ignore the case where finding a match
  2. *exact*: if set, will take only keys that equals key_value (with considerations to case)
  3. If *value_sep* is provided, it is used to separate the value of the element into a list.

XMLPropsFile.writes(props_file=None)
------------------------------------
Writes loaded and possibly updated props into property file
**writes()** will either write a new property file of override existing one with it loaded properties.
*props_file*: a path to property file.  If none provided, the file loaded will be overwritten.
Returns: None
Raises:  XMLPropsWriteFileError

XMLPropsStr.writes()
--------------------
Writes loaded and possibly updated props into property string
**writes()** will either write a new property file of override existing one with it loaded properties.
*props_file*: a path to property file.  If none provided, the file loaded will be overwritten.
Returns: XML formatted string with *entry*, *name and *value* populated from the object


Examples of use
===============

.. code-block:: python

  from xmlprops import XMLPropsStr
  from xmlprops import XMLPropsFile

  ## Define example string
  props_xml_01='''<?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
  <properties>
    <entry key="product">MySql</entry>
    <entry key="service_mode">BF</entry>
    <entry key="exposure">shared</entry>
    <entry key="makers">db1</entry>
    <entry key="max_active">10</entry>
    <entry key="init_active">1</entry>
    <entry key="db1.user">userdb</entry>
    <entry key="db1.password">passworddb</entry>
    <entry key="db1.host">hostdb</entry>
    <entry key="host">hw_host</entry>
    <entry key="db1.port">portdb1</entry>
    <entry key="db1.database">databasedb1</entry>
    <entry key="db2.port">portdb2</entry>
    <entry key="db2.database">databasedb2</entry>
    <entry key="db1.priority">1</entry>
    <entry key="db1.priority">2</entry>
  </properties>
  '''
  ##Load XML from string
  xmlprops=XMLPropsStr(props=props_xml_01)
  print(xmlprops)
  ## prints {'db1.charset': 'utf8', 'db1.use_unicode': 'True', 'init_active': '1', 'product': 'MySql', 'db1.host': 'hostdb', 'service_mode': 'BF', 'db1.port': 'portdb', 'exposure': 'shared', 'db1.password': 'passworddb', 'db1.database': 'databasedb', 'max_active': '10', 'db1.user': 'userdb', 'db1.priority': '2', 'makers': 'db1'}
  xmlprops.get_match(key_prefix='db2.')['port'] ## returns 'portdb2'
  xmlprops.get_match(key_prefix='db1.')['port'] ##returns 'portdb1'
  xmlprops.get_match(key_prefix='db1.port')[''] ##returns 'portdb1'
  xmlprops.get_match(key_prefix='db2.') ## returns OrderedDict([('port', 'portdb2'), ('database', 'databasedb2')])
  ##Next statement examplifies that last value for key "priority" was loaded
  xmlprops.get_match(key_prefix='db1.')['priority'] ## returns '2'
  ## Next statements examplify priority in evaluating keys when using "get" function
  xmlprops.get('db1.host') ## returns 'hostdb' - since key 'db1.host' is evaluated after key 'host' 
  xmlprops.get('db1.max_active') ## returns '10' - key 'max_active' is evaluated first, then 'db1.max_active' is evaluated and is not found
  xmlprops.get('db2.max_active') ## returns '10' - key 'max_active' is evaluated first, then 'db2.max_active' is evaluated and is not found
  xmlprops.set('new_key','new_key_value') ## Add new key/value
  xmlprops.get_contain('host') ## returns {'host': 'hw_host', 'db1.host': 'hostdb'}
  xmlprops.get_contain(key_value='host',exact_match=True) ## returns {'host': 'hw_host'}
  xmlprops.get_contain('db1.host') ## retuns {'db1.host': 'hostdb'}
  xmlprops.get_contain('db.\.port') ## returns {'db2.port': 'portdb2', 'db1.port': 'portdb1'}
  

Additional resources
====================


Documentation is in the "docs" directory and online at the design and use of xmlprops.

**example** and **tests** directory shows ways to use xmlprops . Both directories are available to view and download as part of source code
on GitHub. GitHub_link_

.. _GitHub_link: https://github.com/Acrisel/xmlprops

Docs are updated rigorously. If you find any problems in the docs, or think they
should be clarified in any way, please take 30 seconds to fill out a ticket in
github or send us email at support@acrisel.com

To get more help or to provide suggestions you can send as email to:
arnon@acrisel.com uri@acrisel.com
