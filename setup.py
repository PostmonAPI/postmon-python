try:
    import multiprocessing
except ImportError:
    pass

from setuptools import setup

import postmon

setup(
    name='postmon',
    version=postmon.__version__,
    description='Postmon service wrapper',
    url='http://github.com/PostmonAPI/postmon-python',

    author='Iuri de Silvio',
    author_email='iurisilvio@gmail.com',
    license='MIT',

    py_modules=['postmon'],

    install_requires=[
        'requests>=1.0',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    tests_require=[
        'nose>=1.0',
        'httpretty',
        'mock',
    ],
    test_suite='nose.collector',
)
