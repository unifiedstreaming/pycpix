from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="cpix",
    version="0.0.0",
    description="CPIX",
    long_description=readme,
    author="Mark Ogle",
    author_email="mark@unified-streaming.com",
    packages=find_packages(exclude=("tests", "docs")),
    url="https://github.com/unifiedstreaming/pycpix"
)
