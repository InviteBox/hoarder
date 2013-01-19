import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if os.path.exists('README.rst'):
    long_description = read('README.rst')
else:
    long_description = 'https://github.com/InviteBox/hoarder'

setup(
    name = "hoarder",
    version = "0.0.4",
    author = "Alexander Tereshkin",
    author_email = "atereshkin@invitebox.com",
    description = ("Django analytics kit for the data-obsessed."),
    license = "BSD",
    keywords = "django analytics",
    url = "https://github.com/InviteBox/hoarder",
    packages=['hoarder', ],
    long_description=long_description,
    install_requires=('django-celery'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",        
    ],
    include_package_data=True,
    package_data={'hoarder': ['hoarder/templates']}
)
