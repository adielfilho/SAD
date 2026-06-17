from setuptools import setup, find_packages

setup(
    name='rim_biblioteca',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy', # Dependências da biblioteca
        'json',  
    ],
)