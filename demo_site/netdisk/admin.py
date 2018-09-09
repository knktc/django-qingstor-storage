# -*- coding: utf-8 -*-

"""
use admin to upload file

@author:knktc
@contact:me@knktc.com
@create:2018-09-01 18:22
"""

from django.contrib import admin
from .models import File

__author__ = 'knktc'
__version__ = '0.1'


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'add_time', 'update_time',)
