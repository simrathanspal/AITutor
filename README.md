# AITutor

## Environment setup
For environment setup we use [UV package manager](https://astral.sh/blog/uv) - [Tutorial](https://www.youtube.com/watch?v=qh98qOND6MI).
Project requires Python 3.12
Start by installing UV: `pip install uv`. 

Follow below steps:
1. Setup your environment with: `uv sync`
2. Make a copy of .env_template as .env and fill in your secret keys.


Using virtual environment on VSCode:
1. Open command palette and click on "Python: Select Interpreter"
2. Select the interpreter from the virtual environment created by UV.

Using virtual environment on terminal:
1. Activate the virtual environment with: `source .venv/bin/activate`
