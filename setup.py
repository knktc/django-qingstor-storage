from setuptools import setup

setup(
    name='django_qingstor_storage',
    version='0.1',
    packages=['django_qingstor_storage'],
    url='https://github.com/knktc/django-qingstor-storage',
    license='Apache License 2.0',
    author='knktc',
    author_email='me@knktc.com',
    description='Django storage with Qingstor',
    install_requires=['django>=2.0', 'qingstor-sdk>=2.2.6', ]
)
