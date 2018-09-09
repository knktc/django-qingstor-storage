from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='django_qingstor_storage',
    version='0.1.1',
    packages=['django_qingstor_storage'],
    url='https://github.com/knktc/django-qingstor-storage',
    author='knktc',
    author_email='me@knktc.com',
    description='Django storage with Qingstor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['django>=2.0', 'qingstor-sdk>=2.2.6', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
    ],
)
