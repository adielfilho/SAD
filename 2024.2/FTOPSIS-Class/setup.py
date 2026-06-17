from setuptools import setup, find_packages

setup(
    name='ftopsis_class',
    version='0.1',
    description='FTOPSIS Class implemented in python',
    author='José Ronaldo, Luiz Henrique',
    url='https://github.com/Dev-JoseRonaldo/FTOPSIS-Class',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.1',
        'numpy>=1.26.4',
    ],
)