'''
Created on Nov 26, 2015

@author: arnon
'''
from xmlprops import XMLPropsStr

from xmlprops import XMLProps

props_xml_str='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>

<entry key="Cities">Dallas</entry>
<entry key="Dallas.Schools">Yorkshire</entry>

<entry key="Yorkshire.Head">John</entry>
<entry key="Yorkshire.Phone">214-456-8754</entry>

</properties>
'''

xmlprops=XMLPropsStr(props=props_xml_str)

print(xmlprops.writes())

result=xmlprops.get_keys(prefix="Yorkshire",keys=["Head", "Phone"])

#################

props=XMLProps()
props.loads(props_xml_str, root='properties')
#props.load(props_xml_file_desc, root='properties')

schools=props.get('Dallas.Schools')

props.set('Dallas.Schools', schools + ' Levinta', comment='Schools in Dallas city area')
props.set('Levinta.Head', 'Jordan')
props.set('Levinta.Phone', '214-456-8745')

print( props.dumps() )
#props.dump(file_descp)







