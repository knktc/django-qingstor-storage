# Django Qingstor Storage

A Django storage backend with **Qingstor**.

## Requirements

* Python3
* Django >= 2.0
* qingstor-sdk >= 2.2.6

## Installation

*Using venv is highly recommended.*

Install by PyPI:

```bash

pip install django-qingstor-storage

```

Install by source code, just clone the code, and run following commands to install:

```bash
cd django_qingstor_storage
python setup.py install
```

## Settings

Edit your settings.py and set default(or other name) storage backend:

```python
# set storage backend
DEFAULT_FILE_STORAGE = 'django_qingstor_storage.backends.QinstorStorage'
```

And add Qingstor config in the settings.py:

```python
# Qingstor setting starts here
QINGSTOR_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY_ID'
QINGSTOR_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'
QINGSTOR_ZONE = 'YOUR_QINGSTOR_ZONE'
QINGSTOR_BUCKET = 'YOUR_QINGSTOR_BUCKET'
```

Also, you can set the Qingstor config by setting system environment variables with the following commands:

```bash
export QINGSTOR_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
export QINGSTOR_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
export QINGSTOR_ZONE=YOUR_QINGSTOR_ZONE
export QINGSTOR_BUCKET=YOUR_QINGSTOR_BUCKET
```

## Demo site

We also provide a demo site with Django admin. Just clone the code, edit settings.py in demo_site directory. And use the following commands to make it running:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open your browser to visit <http://localhost:8000> .

## See Also

* Qinstor Python SDK(on github): <https://github.com/yunify/qingstor-sdk-python>
* Qinstor Python SDK docs: <https://docs.qingcloud.com/qingstor/sdk/python/qingstor_sdk.html>
* Qinstor Restful API: <https://docs.qingcloud.com/qingstor/api/>
