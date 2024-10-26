import pathlib
from setuptools import setup

CWD = pathlib.Path(__file__).parent

README = (CWD / "README.md").read_text()

setup(
    name="robotspy",
    version="0.12.0",
    description="Robots Exclusion Protocol File Parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/andreburgaud/robotspy",
    author="Andre Burgaud",
    author_email="andre.burgaud@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=["robots"],
    entry_points={
        "console_scripts": [
            "robots=robots.__main__:main",
        ]
    },
)