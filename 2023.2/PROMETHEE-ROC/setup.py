from setuptools import setup, find_packages

setup(
    name='promethee_ROC',
    version='1.0.0',
    packages=find_packages(),
    author='Luiz Roberto, Penélope Araújo, Luana Cristina, Gabrielle Almeida, João Felipe',
    author_email='lrbf@cin.ufpe.br, pmpa@cin.ufpe.br, lccb@cin.ufpe.br, gao2@cin.ufpe.br, jfbs@cin.ufpe.br',
    description='Uma biblioteca para realizar análises de problema multicritérios com o método PROMETHEE utilizando pesos substitutos com o método ROC',
    url='https://github.com/roboberto1403/promethee_ROC',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy>=1.18.0',
        'matplotlib>=3.0.0'
    ],
)
