# AITutor

## Environment setup
For environment setup we use [UV package manager](https://astral.sh/blog/uv) - [Tutorial](https://www.youtube.com/watch?v=qh98qOND6MI).
Project requires Python 3.12
Start by installing UV: `pip install uv`. 

Follow below steps:
1. Setup your environment with: `uv sync`
2. Make a copy of .env_template as .env and fill in your secret keys.
3. Run command `brew install make` on macOS. 
3. [Download docker](https://www.docker.com/products/docker-desktop/) if not already available, install and open it.
4. Set up [GitHub co-pilot for free](https://docs.github.com/en/copilot/managing-copilot/managing-copilot-as-an-individual-subscriber/managing-copilot-free/about-github-copilot-free)
5. Run command `make local-db-up` to start the local MongoDB database.


#### Setting up virtual environment on VSCode
1. Open command palette and click on "Python: Select Interpreter"
2. Select the interpreter from the virtual environment created by UV.

#### Setting up virtual environment on Terminal
1. Activate the virtual environment with: `source .venv/bin/activate`


#### Docker commands
1. List all running containers: `docker ps`
2. Stop all running containers: `docker stop $(docker ps -q)`

