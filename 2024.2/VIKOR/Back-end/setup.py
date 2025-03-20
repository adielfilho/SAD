from setuptools import setup, find_packages

setup(
    name='vikor',
    version='0.1.0',
    description='Implementação do método VIKOR para tomada de decisão multicritério',
    author='Gustavo Silva, Eraldo Cassimiro, Arlen Filho, Hyan Silva',
    author_email='gds4@cin.ufpe.br, afsf2@cin.ufpe.br,hlvs@cin.ufpe.br,ejces@cin.ufpe.br',
    url='https://github.com/GustavoDiego/SAD/tree/main/2024.2/VIKOR',
    packages=find_packages(), 
    install_requires=[
       'colorama==0.4.6',
        'iniconfig==2.0.0',
        'packaging==24.2',
       'pluggy==1.5.0',
        'pytest==8.3.5',
        'setuptools==76.0.0'

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License', 
    ],
    python_requires='>=3.13',  
)
