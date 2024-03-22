from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='TOPSIS-Sort-C',
    version='0.1.1',
    license='MIT License',
    description='TOPSIS-Sort-C implemented in python',
    long_description=readme,
    long_description_content_type="text/markdown",
    author=['Gustavo Hollanda', 'Geovanna Domingos', 'Giovanna Machado', 'Higor Cunha', 'Maria Eduarda Melo'],
    author_email=['ghcs@cin.ufpe.br', 'gmdomingosn@gmail.com', 'gpmb@cin.ufpe.br', 'hbc@cin.ufpe.br', 'meomcin.ufpe.br'],
    url='https://github.com/gustavo-ghcs/TOPSIS-Sort-C',
    install_requires=[
        'numpy>=1.26.4',
    ],
)