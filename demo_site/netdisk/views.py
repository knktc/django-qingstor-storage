# -*- coding: utf-8 -*-

"""
Use default storage to manipulate files

@author:knktc
@contact:me@knktc.com
@create:2018-09-01 18:22
"""

from django.http import HttpResponse, Http404
from django.core.files.storage import DefaultStorage
from django_qingstor_storage.backends import Qinstor404Exception as FileDoesNotExistException


STORAGE = DefaultStorage()


def download(request, **kwargs):
    """ download file, no need to change codes when you change the storage backend
    """
    filename = kwargs.get('filename')
    try:
        f = STORAGE.open(filename)
    except FileDoesNotExistException:
        raise Http404

    response = HttpResponse(f.read())
    return response
