# Black Hack Python - 2nd edition

## Configure *virtual environment*

```sh
# Create virtual environment with name venv3
python3 -m venv vnev3

# Activate virtual environment
source venv3/bin/activate

# Deactivate virtual environment
deactivate

```

### Run script as sudo

```sh
sudo env "PATH=$PATH VIRTUAL_ENV=$VIRTUAL_ENV" python <script>
```

## Manage dependencies

### Update requirements.txt

```sh
python -m pip freeze > requirements.txt
```

### Install dependencies

After activate the vitual environment

```sh
python -m pip install -r requirements.txt
```

