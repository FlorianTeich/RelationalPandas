"""
Setup.py
"""

from setuptools import setup, find_packages

setup(
    name="relationalpandas",
    version="1.0",
    description="relationalpandas",
    author="Florian Teich",
    author_email="florianteich@gmail.com",
    url="https://github.com/FlorianTeich/RelationalPandas",
    packages=find_packages(include=["relationalpandas", "relationalpandas.*"]),
    python_requires=">=3.6",
    install_requires=[
        "xxhash>=3.1.0",
        "pandas>=1.5.1",
        "numpy>=1.23.4",
        "matplotlib>=3.6.2",
        "networkx>=2.8.8",
    ],
)
