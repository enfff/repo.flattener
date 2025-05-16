# Repo Flattener

Flattens out one or more GitHub repositories, and converts them into `.txt` files that can be fed to LLMs

Example usage

    flatten.py [-h] urls [urls ...]

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