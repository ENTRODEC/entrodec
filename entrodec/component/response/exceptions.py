# _*_ coding: utf-8 _*_
from __future__ import unicode_literals

__author__ = 'Dmitri Meshin <dmitri.meshin@gmail.com>'


class NotFoundException(BaseException):
    def __init__(self, *args, **kwargs):
        super(NotFoundException, self).__init__(kwargs)

