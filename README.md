# Local Video Library

A GUI for managing and watching locally downloaded movies and TV shows on your computer.

The main components are as follows:
- A GTK user interface that displays your library
- Communications with an online database for metadata collection
- Local database for information and offline usage

### Members:
- Alex Reynen (a_reynen@u.pacific.edu)
- Austin Whyte (a_whyte@u.pacific.edu)

## Development Environment Setup

### Requirements

- Python 3.9
- GTK
- pipenv (`pip install pipenv`)

1. Install dependencies: `pipenv install --site-packages`
2. (Optional) Install development dependencies: `pipenv install --dev`
3. Activate the virtualenv with `pipenv shell`

## Running Local Video Library

### Requirements

- Python 3.9
- Pip
- Git
- GTK (will already be installed on most \*nix graphical enviornments)
1. In a terminal, run the following: `pip install git+https://github.com/comp195/spring-2021-final-project-we-use-arch-btw.git@main#egg=LVL`

LVL will now be installed in `~/.local/bin`

To run, in a terminal execute `lvl`
