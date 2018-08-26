# -*- coding: utf-8 -*-

_author = 'Mike Burr'
_email = 'mburr@unintuitive.com'
__author__ = '%s <%s>' % (_author, _email)

from distutils.core import setup
import time

# my modules
import svg_graph

# README.rst dynamically generated:
with open('README.md', 'w') as f:
    f.write(svg_graph.__doc__)

NAME = svg_graph.__name__

def read(file):
    with open(file, 'r') as f:
        return f.read().strip()

setup(
    name=NAME,
    version='0.0.1-%s' % time.time(),
    long_description=read('README'),
    author=_author,
    author_email=_email,
    provides=[NAME],
    packages=[NAME],
)
