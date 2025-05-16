# Repo Flattener

Flattens out one or more GitHub repositories, and converts them into `.txt` files that can be fed to LLMs


Given this Example repository

    example-repo
    ├── folder
    │   ├── file.py
    |   ├── __init__.py
    │   └── subfolder
    │       └── hello.py
    └── README.md

The output is

    example-repo.folder.file.txt
    example-repo.folder.subfolder.hellp.txt
    example-repo.README.txt


**Features**

- Blacklist folders, files and extensions


## How to use

Download the repo, create and use the virtual environment

``` bash
    git clone https://github.com/enfff/repo.flattener
    cd repo.flattener/
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt
```

Example usage

    flatten.py [-h] urls [urls ...]