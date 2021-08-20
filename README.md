# Restbucks
An RESTful django development challenge for managing a small coffee shop.


## Commands
~~~~~~~~
git clone https://github.com/M-b850/Restbucks.git
cd Restbucks/
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata fixtures/store.json
./manage.py runserver

:) Enjoy.
~~~~~~~~

## TODO
1. Tests for client app. [  ]
2. Make Tag choices more clean in code. [  ]
3. Clean admin.py and use comments. [  ]
