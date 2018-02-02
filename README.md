# Oracle Server

0. python3 is required.
1. Build python virtualenv. (Don't use ./setup_venv.sh now, there are some bugs to be solved.)
2. Launch virtual env, and install all dependency in requirements.txt.
	$ pip install -r requirements.txt
3. Copy and modify ./oracle/.env.default, and store as a new file with this path: ./oracle/.env.
4. If the built is just for testint, you can just use sqlite rather than MYSQL. Modify DB settings in ./oracle/settings/base.py as below:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

5. Get all submodules in this repo.

$ git submodule init

$ git submodule update

6. Migrate DB and run server.

$ cd <ORACLE_PATH>/oracle

$ ./manage.py migrate

$ ./manage.py runserver 0.0.0.0:(port_num)
