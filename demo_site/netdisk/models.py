# -*- coding: utf-8 -*-

"""
demo netdisk models

@author:knktc
@contact:me@knktc.com
@create:2018-09-01 18:11
"""

from django.db import models

__author__ = 'knktc'
__version__ = '0.1'


class File(models.Model):
    filename = models.FileField()
    note = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
