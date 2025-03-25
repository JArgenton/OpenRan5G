from setuptools import setup, find_packages

setup(
    name="meu_projeto",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "teste_open=programer.main:main", 
        ],
    },
)
