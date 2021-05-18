from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="cpix",
    version="1.1.4",
    description="CPIX",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Mark Ogle",
    author_email="mark@unified-streaming.com",
    packages=find_packages(exclude=("tests", "docs")),
    url="https://github.com/unifiedstreaming/pycpix",
    include_package_data=True,
    install_requires=[
        "construct >= 2.9.45",
        "lxml >= 4.2.3",
        "protobuf >= 3.3.0",
        "pycryptodome >= 3.6.4",
        "requests >= 2.19.1",
        "isodate >= 0.6.0"
    ]
)
