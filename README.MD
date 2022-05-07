To create the virtial environment

    python -m venv `<name>`

To activate virtial env inside of terminal

    source venv/bin/activate

To check dependencies in project

    pip list

or

    pip freeze

To lock depedencies into requirements.txt

    pip freeze >> requirements.txt

To install fastapi, don't run `pip install fastapi[all]`.
The problem is that in zsh, contrary to bash [ and ] have special meaning. You need to use quotes: `pip install 'fastapi[all]'` or` escape them pip install fastapi\[all\]`

To run the project

    uvicorn main:app

main is file name eg `main.py`, app is instance name intialized in code like `app = FastAPI() `

To run project while listening to changes

    uvicorn main:app --reload

To access swagger ui docs

    http://127.0.0.1:8000/docs

To access redoc docs

    http://127.0.0.1:8000/redoc
