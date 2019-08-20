from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'deform',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_tm',
    'pymongo',
    'sqlalchemy',
    'alembic',
    'waitress',
    'zope.sqlalchemy',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest'
]

setup(
    name='deepersystems',
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    },
    entry_points={
        'paste.app_factory': [
            'main = deepersystems:main'
        ],
        'console_scripts': [
            'initialize_deepersystems_db = deepersystems.initialize_db:main'
        ],

    }
)

