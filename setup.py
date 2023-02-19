from setuptools import setup
from pyattr import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pyattr",
    version=__version__,
    author="skifli",
    url="https://github.com/skifli/pyattr",
    project_urls={
        "Documentation": "https://github.com/skifli/pyattr#example",
        "Source": "https://github.com/skifli/pyattr",
    },
    description="Proper access modifiers for Python classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=["pyattr"],
)
