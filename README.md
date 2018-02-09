# An OIDCFed Signing Service

## Installation

Pull the git repo:

~~~bash
git clone https://github.com/daserzw/fedoidc_ss.git
~~~

Create a virtualenv and activate it:

~~~bash
cd fedoidc_ss
python3 -mvenv venv
. venv/bin/activate
~~~

Install the required libraries:

~~~bash
pip install fedoidc flask sqlalchemy
~~~

## Configuration

The application is configured through a python file, `fedoidc_ss/config.py`:

~~~python
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# DEBUG
DEBUG = True
TRAP_BAD_REQUEST_ERRORS = True

# DB
SQLITE_DB_PATH='sqlite:///' + os.path.join(_basedir, 'data/app.data')

# ENTITY AND SIGNING
FO_NAME = 'https://fo.org'
FO_SIG_KEYS = os.path.join(_basedir, 'data/fo_org.jwks')
CREATE_FO_JWKS = False
FO_SIG_LIFETIME = 300

# KEYDEFS
KEYDEFS = [
    {"type": "RSA", "key": '', "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]}
]
~~~

You want to change the name of the Federation Operator, `FO_NAME`.
Also, you need to add a JWKS containing the key set you want to use 
to sign metadata_statements (default location is `data/fo_org.jwks`). 

## Running

Activate the virtualenv and execute the run.py file:

~~~bash
cd fedoidc_ss
. venv/bin/activate
python run.py
~~~

## Usage

Coming...

