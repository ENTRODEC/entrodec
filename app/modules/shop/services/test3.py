# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'

def test3():
    #print 'TEST 3'
    return 'TEST3RET'


class test3class:

    def __init__(self, some):
        #print some
        pass

    def testmethod(self, arg1, arg2):
        pass
        #print arg1, arg2

    def set_alchemy(self, create_engine):
        engine = create_engine('sqlite:///:memory:')
        engine.execute("select 'This is sqlalchemy SQL String!'").scalar()