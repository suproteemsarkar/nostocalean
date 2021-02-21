"""Set up the package."""

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="nostocalean",
    version="0.0.1",
    author="Suproteem Sarkar",
    packages=["nostocalean", "nostocalean.ols"],
    python_requires=">=3.5",
    description="Custom utility functions.",
    long_description=long_description,
    url="https://github.com/suproteemsarkar/nostocalean",
    license="MIT",
)
