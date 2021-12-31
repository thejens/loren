import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loren",
    version="0.0.4",
    author="Jens Larsson",
    author_email="jens.larsson56@gmail.com",
    description="A package with a powerful config parser and file renderer", # noqa E501
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thejens/loren",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
