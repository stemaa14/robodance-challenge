import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

requires = [
    'pyramid',
    'pyramid_tm',
    'pyramid_zodbconn',
    'transaction',
    'ZODB3',
    'waitress',
    'persistent',
    'BTrees',
    'zodburi',
    'ZODB'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    ]

setup(name='robodance',
      version='1.0',
      description='robodance',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Max Stebner',
      author_email='stemaa14@htl-kaindorf.ac.at',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = robodance:main
      """,
      )
