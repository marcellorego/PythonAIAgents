In order to run the code, you need to do the following steps:

1. Make sure you have Python 3.7 installed and `python3.10-venv` package
```commandline
make add-venv
```
2. Clone the repository
3. Create a virtual environment
```commandline
make env
```
4. Activate the virtual environment
```commandline
source $(make act)
```
5. Install the requirements
```commandline
make deps
```
6. Run the code
```commandline
make run
```
7. Deactivate the virtual environment
```commandline
$(make dact)
```
