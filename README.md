# deepersystems
## Deeper Systems Test

## Prerequisites
* Python 3.5
* MongoDB installed and activated


## Instructions to install:
1. Clone the repository

1. _cd_ into deepersystems directory

1. Create and activate a virtualenv
 
    ```
    $ python3 -m venv env
    $ source env/bin/activate
    ```

1. Upgrade pip and setuptools

    ```
    $ pip install --upgrade pip setuptools
    ```

1. Install packages

    ```
    $ pip install -e ".[dev]"
    ```

1. Serve the application

    ```
    $ pserve development.ini --reload
    ```

1. Open URL displayed in the browser