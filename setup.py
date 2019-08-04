import os
from setuptools import find_packages, setup

import action_serializer


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='drf-action-serializer',
    version=action_serializer.__version__,
    packages=find_packages(),
    install_requires=['Django>=2', 'djangorestframework>=3'],
    description='A serializer that handles field configuration with multiple actions from ViewSets.',
    long_description=long_description,
    url='https://github.com/gregschmit/drf-action-serializer',
    author='Gregory N. Schmit',
    author_email='schmitgreg@gmail.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
