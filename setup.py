from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="galshaya-chorder",
    version="0.1.1",
    author="Gal Shaya",
    author_email='isaiahgal@gmail.com',
    description="A command-line tool for formatting and transposing chord charts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galshaya/chorder",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Text Processing",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "chorder=chorder.main:main",
        ],
    },
) 