# Oracle Server

0. 請用python3
1. 架設python virtualenv(請先忽略./setup_venv.sh，有些小問題待修復)
2. 切到 virtualenv 中，安裝 requirements.txt 中的套件。
	$ pip install -r requirements.txt
3. 修改./oracle/.env.default，設定完後另存為./oracle/.env
4. 如測試用，可以將./oracle/settings/base.py 中的 DB 設定成 sqlite。改為以下：

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

5. 增加smart contract submodule:

$ git submodule init
$ git submodule update

6.
$ cd <ORACLE_PATH>/oracle
$ ./manage.py migrate
$ ./manage.py runserver 0.0.0.0:(port_num)