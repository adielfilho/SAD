from setuptools import setup, find_packages

setup(
    name='ftopsis_class',
    version='0.1',
    description='FTOPSIS Class implemented in python',
    author='Lucas C., Ian F., Matheus F., Rodrigo B., Arthur C.',
    url='https://github.com/lucasccampos/ftopsis_class',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.1',
        'numpy>=1.26.4',
    ],
)