"""Set up the package."""

from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name="nostocalean",
    version="0.0.11",
    author="Suproteem Sarkar",
    packages=find_packages(),
    python_requires=">=3.5",
    description="Custom utility functions.",
    long_description=long_description,
    url="https://github.com/suproteemsarkar/nostocalean",
    license="MIT",
)
