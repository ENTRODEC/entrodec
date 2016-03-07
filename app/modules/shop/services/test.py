# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'

def test(name, value):
    """

    :param name: str
    :param value: str
    :return: str
    """

    #print 'Hello, %s' % name
    #print value
    return '<h1>This is the test: %s</h1>' % name

class test_class:

    def foo(self):
        #print 'Foo from test class'
        pass