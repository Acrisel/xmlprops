import os
import sys

from setuptools import setup
from distutils.sysconfig import get_python_lib

# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Accord are
# still present in site-packages. See #18115.
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, 'xmlprops'))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break

setup_info={'name': 'xmlprops',
 'version': '2.0.0',
 'url': 'https://github.com/Acrisel/xmlprops',
 'author': 'Acrisel Team',
 'author_email': 'support@acrisel.com',
 'description': 'XMLProps allows the use XML based properties files similar '
                'to Java.',
 'long_description': '========\n'
                     'xmlprops\n'
                     '========\n'
                     '\n'
                     'xmlprops provides means to access properties that are '
                     'stored in XML (file or string).  \n'
                     'There are two main classes xmlprops provides:\n'
                     '1. XMLPropsFile: file based XML that containing '
                     'properties\n'
                     '2. XMLPropsStr: string base XML that containing '
                     'properties\n'
                     '\n'
                     'Thes class provides methods to would comfirtably allow '
                     'access to the properties stored.\n'
                     '\n'
                     'More information in README document.\n'
                     '\n'
                     'We hope you would enjoy using this package.  Let us '
                     'know your experiecne.\n'
                     '\n'
                     'The Acrisel Team.',
 'license': 'MIT',
 'keywords': 'project, virtualenv, parameters',
 'packages': ['xmlprops'],
 'install_requires': ['wheel>=0.24.0'],
 'extras_require': {'dev': [], 'test': []},
 'classifiers': ['Development Status :: 5 - Production/Stable',
                 'Environment :: Other Environment',
                 'Framework :: Project Settings and Operation',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Software Development :: Libraries :: Application '
                 'Frameworks',
                 'Topic :: Software Development :: Libraries :: Python '
                 'Modules']}
setup(**setup_info)


if overlay_warning:
    sys.stderr.write("""

========
WARNING!
========

You have just installed XMLProps over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
Accord. This is known to cause a variety of problems. You
should manually remove the

%(existing_path)s

directory and re-install XMLProps.

""" % {"existing_path": existing_path})
