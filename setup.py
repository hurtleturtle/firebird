from setuptools import setup, find_packages


setup(
    name='firebird',
    version='1.0.1',
    author='Jono Nicholas',
    description='Graphing of monitored events',
    packages=['firebird'],
    install_requires=[
        'asyncio',
        'websockets'
    ],
    entry_points={
        'console_scripts': [
            'firebird = firebird.watcher:run'
        ]
    }
)