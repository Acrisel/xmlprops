'''
Created on Oct 13, 2013

@author: arnon
'''
import xml.etree.ElementTree as etree
import os.path
from .expandvars import expandvars
from collections import OrderedDict
from collections import Mapping
import re
import base64

try:
    from projenv import Environ
    found_environ=Environ
except ImportError:
    found_environ=None
    
class XMLPropsError(Exception):
    pass
    
class __XMLProps(dict):
    '''
    xmlprops reads and manipulate properties file Java XML style
    It keeps properties and provides service to pick them
    
    init accepts a properties file to read.  
        
    If file doesn't exists, it is assumes that 
    a new properties file is to be created.
        
    The get dict function '[]' was enhanced to include hierarchical get.
    on the item a.b.c; get will try to get c, a.c, and a.b.c.
    The last one available, wins.
    
    The write() function updates 
    '''
    
    def __init__(self, root, environ=None, key_sep='.', decrypt_method=None, decrypt_params={}): 
        '''
            Initialize properties object out of conf_file
            Parameters:
                conf_file: properties file to load
                environ: environment by which to translate values
                sep: default separator to use as key parts separator
        '''
        super().__init__()
        
        self.key_sep=key_sep if key_sep is not None else '.'
        # TODO: ensure env is defined is this logic tree
        if environ is None:
            env=OrderedDict()
        elif isinstance(environ, Mapping):
            env=OrderedDict(environ)
        elif found_environ is not None and isinstance(environ, Environ):
            env=environ._asdict()
                
        for entry in root.findall('entry'):
            key=entry.attrib['key']
            value=expandvars(entry.text, env)
            super().__setitem__(key, value)
            env[key]=value
            
    def set(self, key, value):
        super().__setitem__(key, value)
            
    def get(self, key, key_sep=None):
        '''
        The get dict function '[]' was enhanced to include hierarchical get.
        on the item a.b.c; get will try to get c, a.c, and a.b.c.
        The last one available, wins.
        '''
        key_sep=key_sep if key_sep is not None else self.key_sep
        kpart = key.split(key_sep)
        kname = kpart[len(kpart)-1]
        kpath_part = ['']
        if len(kpart) > 1:
            kpath_part[len(kpath_part):] =  kpart[0:len(kpart)-1]
        kpath = ''
        value = None
        for part in kpath_part:
            if part != '':
                kpath = kpath+part
            if kpath != '':
                kpath = kpath + key_sep
            name = kpath + kname
            this_value = super().get(name)
            if this_value:
                value = this_value
        return value
    
    def get_keys(self, prefix, keys, key_sep=None):
        key_sep=key_sep if key_sep is not None else self.key_sep
        result=dict(map(lambda x: (x, self.get('{p}{s}{k}'.format(p=prefix, s=key_sep, k=x))), keys))
        return result
                
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        return self.set(key, value)
    
    def __set(self, store, name, value, decrypt=False):
        store[name]=value
        if name.endswith('_encrypted') and decrypt:
            decrypted_name, _, _ = name.rpartition('_')
            decrypted_value=value=base64.b64decode(value).decode()
            store[decrypted_name]=decrypted_value
            
    def get_by_fix(self, key_prefix=None, key_suffix=None, key_sep=None, value_sep = None, decrypt=False):
        '''
        Key is found if it has prefix and suffix 
        Each key found is loaded into a dictionary
        The key used in the returned dictionary is stripped of its prefix.
        The function returns this newly created dictionary
        If you want the prefix to end with '.' delimiter; use 'prefix.'
        as key_prefix.
        
        If value_sep provided, it is used to separate the value of the element
        into a list.
        
        If decrypt, encrypted fields with ending with _encrypted will be decrypted
        '''
        key_sep=key_sep if key_sep is not None else self.key_sep
        this_dict = OrderedDict()
        for dict_key in self.keys():
            found_prefix=True if key_prefix is None else dict_key.startswith(key_prefix)
            found_suffix=True if key_suffix is None else dict_key.endswith(key_suffix)
            if found_prefix and found_suffix:
                this_key = dict_key[len(key_prefix):]
                value = super().get(dict_key)
                if value_sep:
                    value_sep = value.split(value_sep)
                self.__set(store=this_dict, name=this_key, value=value, decrypt=decrypt)
                
        return this_dict
    
    def get_by_re(self, key_re=None, value_sep = None, decrypt=False):
        ''' 
        Looks for keys that fits regular expression.
        
        key_re is string of a Pythonic regular expression        
        If value_sep provided, it is used to separate the value of the element
        into a list.
        '''
        
        re_obj=re.compile(key_re)
        this_dict = dict()
        for dict_key in self.keys():
            found_re=True if key_re is None else re_obj.search(dict_key)
            if found_re:
                this_key = dict_key
                value = super().get(dict_key)
                if value_sep:
                    value_sep = value.split(value_sep)
                
                self.__set(store=this_dict, name=this_key, value=value, decrypt=decrypt)
        return this_dict
    
    def get_if_has(self, key_value=None, ignore_case=False, exact_match=False, value_sep = None, decrypt=False):
        ''' 
        Looks for keys that that has key_value in them.
        
        ignore_case: if set will ignore the case where finding a match
        exact: if set, will take only keys that equals key_value (with 
        considerations to ignore case)
        
        If value_sep provided, it is used to separate the value of the element
        into a list.
        '''
        
        if ignore_case:
            key_value=key_value.lower()
            
        if exact_match:
            if ignore_case:
                method=lambda x: x.lower() == key_value
            else:
                method=lambda x: x == key_value
        else: # exact_match
            re_obj=re.compile(key_value)
            if ignore_case:
                method=lambda x: re_obj.search(x.lower()) is not None
            else:
                method=lambda x: re_obj.search(x) is not None
            
        this_dict = dict()
        for dict_key in self.keys():
            found_re=True if key_value is None else method(dict_key)
            if found_re:
                this_key = dict_key
                value = super().get(dict_key)
                if value_sep:
                    value_sep = value.split(value_sep)
                
                self.__set(store=this_dict, name=this_key, value=value, decrypt=decrypt)
        return this_dict
    
    def write(self, props_file=None):
        doc=etree.ElementTree()
        for name, value in self.items():
            doc.Element(tag='entry', attrib={'name':name, 'value':value} )
        doc_file=self.conf_file if props_file is None else props_file
        if doc_file is not None:
            doc.write(doc_file)
            

class XMLPropsFile(__XMLProps):
    '''
    xmlprops reads and manipulate properties file Java XML style
    It keeps properties and provides service to pick them
    
    init accepts a properties file to read.  
        
    If file doesn't exists, it is assumes that 
    a new properties file is to be created.
        
    The get dict function '[]' was enhanced to include hierarchical get.
    on the item a.b.c; get will try to get c, a.c, and a.b.c.
    The last one available, wins.
    
    The write() function updates 
    '''
    
    def __init__(self, props, environ=None, key_sep='.', decrypt_method=None, decrypt_params={}): 
        '''
            Initialize properties object out of props as string
            Parameters:
                props: properties file to parse
                environ: environment by which to translate values
                key_sep: default separator to use as key parts separator
        '''
        
        # first load default file provided by path
        # will point to: /var/ezcoord/ezcoord.properties
        if  os.path.exists(props):
            #print('loading configuration file {file}'.format(file=conf_file))
            try:
                tree=etree.parse(props)
            except Exception as e:
                raise Exception('failed to open file: {}; {}'.format(props, repr(e)))
            try:
                root=tree.getroot()
            except Exception as e:
                raise Exception('failed to parse XML: {}'.format(repr(e)))
        else:
            raise XMLPropsError('Props file {} not found'.format(props))
        
        super().__init__(root=root, environ=environ, key_sep=key_sep)
 

class XMLPropsStr(__XMLProps): 
    def __init__(self, props, environ=None, key_sep='.', decrypt_method=None, decrypt_params={}): 
        '''
            Initialize properties object out of props as string
            Parameters:
                props: properties string to load
                environ: environment by which to translate values
                key_sep: default separator to use as key parts separator
        '''
        
        root=etree.fromstring(props)           
        
        super().__init__(root=root, environ=environ, key_sep=key_sep)
