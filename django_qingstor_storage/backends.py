# -*- coding: utf-8 -*-

"""
Qinstor storage backend

@author:knktc
@contact:me@knktc.com
@create:2018-08-31 15:41
"""

import base64
import hmac
import os
import time
import urllib
from hashlib import sha256
from tempfile import SpooledTemporaryFile

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File
from django.core.files.storage import Storage
from qingstor.sdk.config import Config
from qingstor.sdk.service.qingstor import QingStor

__author__ = 'knktc'
__version__ = '0.1'


def _get_config(name):
    """ get config from env and settings
    """
    # from env
    value = os.environ.get(name, getattr(settings, name, None))
    if value:
        return value
    else:
        raise ImproperlyConfigured('{} should be set in env or settings.py'.format(name))


class QinstorException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Qinstor404Exception(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class QinstorStorage(Storage):
    def __init__(self, access_key_id=None, secret_access_key=None, zone=None, bucket_name=None):
        self.access_key_id = access_key_id if access_key_id else _get_config('QINGSTOR_ACCESS_KEY_ID')
        self.secret_access_key = secret_access_key if secret_access_key else _get_config('QINGSTOR_SECRET_ACCESS_KEY')
        self.zone = zone if zone else _get_config('QINGSTOR_ZONE')
        self.bucket_name = bucket_name if bucket_name else _get_config('QINGSTOR_BUCKET')

        # get bucket
        config = Config(self.access_key_id, self.secret_access_key)
        qingstor = QingStor(config)
        self.bucket = qingstor.Bucket(bucket_name=self.bucket_name, zone=self.zone)

        # todo check bucket existence

    def _get_share_link(self, name, expires=60 * 5):
        """ get share link, so user can download file directly from qingstor with this link
        about signature: https://docs.qingcloud.com/qingstor/api/common/signature.html

        :param name: object key
        :param expires: link expires time, in seconds(default 5 minutes)
        :return: url
        :rtype: str
        """
        expires = int(time.time()) + expires
        string_to_sign = 'GET\n' \
                         + '\n' \
                         + '\n' \
                         + '{}\n'.format(expires) \
                         + '/{}/{}'.format(self.bucket_name, name)
        host = 'https://{}.{}.qingstor.com'.format(self.bucket_name, self.zone)

        h = hmac.new(
            self.secret_access_key.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            digestmod=sha256
        )
        signature = base64.b64encode(h.digest()).strip()

        url = '{}/{}?expires={}&{}&access_key_id={}&'.format(host, name, expires,
                                                             urllib.parse.urlencode({'signature': signature}),
                                                             self.access_key_id)
        return url

    def _save(self, name, content):
        """ store file into qingstor
        
        :param name: object key for the file to store
        :param content: file object
        :return: object key
        :rtype: str
        """
        output = self.bucket.put_object(object_key=name, body=content)

        if output:
            raise QinstorException('code:{}, message:{}'.format(output.get('code'), output.get('message')))

        return name

    def _open(self, name, mode='rb'):
        """ open file and return file object

        :param name: file name
        :param mode: keep it to rb
        :return: django file wrapper
        :rtype: object
        """
        if mode != "rb":
            raise ValueError("only read-only mode allowed")

        tmp_file = SpooledTemporaryFile(max_size=1024 * 1024 * 10)
        resp = self.bucket.get_object(name)

        # check if file exists
        if resp.status_code == 404:
            raise Qinstor404Exception('object {} does not exist'.format(name))

        for chunk in resp.iter_content():
            tmp_file.write(chunk)
        tmp_file.seek(0)
        return QingstorFile(tmp_file, name, self)

    def exists(self, name):
        """ always return False right now...
        """
        # todo check file existence

        return False

    def url(self, name, expires=60 * 5):
        """ not sure is there any way to get a signed url by the sdk,
        So I have to write a function to get the share link
        """
        return self._get_share_link(name=name, expires=expires)

    def delete(self, name):
        """ delete object from qingstor
        """
        self.bucket.delete_object(name)


class QingstorFile(File):

    """
    A file returned from Qingstor
    """

    def __init__(self, file, name, storage):
        super(QingstorFile, self).__init__(file, name)
        self._storage = storage

    def open(self, mode="rb"):
        if self.closed:
            self.file = self._storage.open(self.name, mode).file
        return super(QingstorFile, self).open(mode)
