import os
from setuptools import find_packages, setup
from action_serializer import version


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# stamp the package prior to installation
version.stamp_directory('./action_serializer')

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='drf-action-serializer',
    version=version.get_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data={'action_serializer': ['VERSION_STAMP']},
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

# un-stamp the package after installation
version.unstamp_directory('./action_serializer')
