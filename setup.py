from setuptools import setup, find_packages


setup(
    name='firebird',
    version='1.0.1',
    author='Jono Nicholas',
    description='Graphing of monitored events',
    packages=['firebird'],
    py_modules=['wsgi'],
    install_requires=[
        'aiofiles==23.1.0',
        'click==8.1.3',
        'Flask==2.2.3',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.2',
        'PyYAML==6.0',
        'watchdog==2.3.1',
        'websockets==10.4',
        'Werkzeug==2.2.3',
    ],
    entry_points={
        'console_scripts': [
            'firebird = firebird.comms:run'
        ]
    }
)