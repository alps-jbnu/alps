import os

from setuptools import setup, find_packages


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


install_requires = {
    'alembic >= 0.7.4',
    'click >= 3.3',
    'Flask >= 0.10.1',
    'SQLAlchemy >= 0.9.8',
}

tests_require = {
    'pytest >= 2.6.4'
}

docs_require = {
    'Sphinx >= 1.2.3'
}

setup(
    name='alps',
    version='0.0',
    description='ALPS website',
    long_description=readme(),
    url='https://github.com/alps-jbnu/alps',
    author='ALPS group',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.4',
        'Framework :: Flask',
    ],
    packages=find_packages(exclude=['tests']),
    package_data={
        'alps': [
            'migrations/env.py',
            'migrations/script.py.mako',
            'migrations/versions/*.py'
        ]
    },
    install_requires=install_requires,
    extras_require={
        'docs': docs_require,
        'tests': tests_require,
    },
    entry_points='''
        [console_scripts]
        alps = alps.cli:main
    ''',
)
