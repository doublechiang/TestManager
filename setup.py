import os,sys
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

sys.path.insert(0, (os.path.join(os.path.dirname(__file__),'src')))

from version import Version

setuptools.setup(
    name='utm',  
    version=str(Version()),
    author="Jiang Junyu",
    author_email="chunyu.chiang@qmfremont.com",
    description="UUT Test Manger on PXE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doublechiang/UTM",
    packages=['utm'],
    # package_dir def: key is the name and values is the directory
    # mapping '' root package to a folder. or mapping package to 'src' folder

    package_dir={'utm': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='UUT Test Manager',
    install_requires=['flask', 'gunicorn', 'flask-restful', 'flask_apispec', 'watchdog']
 )
