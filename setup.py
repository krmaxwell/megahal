#!/usr/bin/env python

"""Setup script for py-megahal"""

def main():
    from distutils.core import setup

    setup(name='megahal',
          author='Chris Jones',
          author_email='cjones@gruntle.org',
          url='http://gruntle.org/projects/python/megahal/',
          description='Python implementation of megahal markov bot',
          license='BSD',
          version='0.2',
          py_modules=['megahal'],
          scripts=['scripts/megahal'],

          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: BSD License',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 2.6',
              'Topic :: Education',
              'Topic :: Scientific/Engineering :: Artificial Intelligence',
              'Topic :: Software Development :: Libraries :: Python Modules'])

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
