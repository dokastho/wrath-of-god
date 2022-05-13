"""
Wrath of God, breaker of Comcast.

Thomas Dokas <dokastho@umich.edu>
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='wog',
    version='0.1.0',
    author="Thomas Dokas",
    author_email="dokastho@umich.edu",
    description="Wrath of God, breaker of Comcast.",
    url="https://github.com/dokastho/wrath-of-god",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['src']),
    include_package_data=True,
    install_requires=[],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'wog = src.__main__:main'
        ]
    },
)
