# Recipes for stacklands game

The site describes recipes from staclands game `v1.1.6`.

## Prepare

Python 3.10 is required for the project.

1. Create and activate virtual environment.

    ```console
    python -m venv venv

    .venv/Scripts/Activate.ps1
    ```

2. Install requirements.

    ```console
    pip install -r requirements.txt
    ```

3. Activate script for prepare icons.

    ```console
    python .\scripts\create_icons.py
    ```

## Run server

```console
    flask run
```
