## Introduction

### Installation

The recommended way is to use [pyenv](https://github.com/pyenv/pyenv) to manage python versions and [poetry](https://python-poetry.org/docs/) to install, manage python dependencies, build virtual environments, build and publish your packages.

1. Install `pyenv` by following instructions in the official [README.me](https://github.com/pyenv/pyenv/blob/master/README.md) file
2. Install `poetry` by following its [official documentation](https://python-poetry.org/docs/#installation)
3. Install `python == 3.12` with 
```shell
make python
```
4. Setup venv by running
```shell
make env
```
That's it!
