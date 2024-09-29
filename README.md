# Django channels socket example app

#### setup and install

`pip install -r requirements.txt`

#### migrate

`python manage.py migrate`

#### run

`daphne -b 0.0.0.0 -p 8001 progress_app.asgi:application`

#### open

[http://localhost:8001/](http://localhost:8001/)

### [code snippets](/deets.md)

### If you want HTTP/2 support and TLS support

- install `pip install Twisted[http2,tls]`
- your requirements.txt should look like

```txt
Django==4.2.5
channels==4.0.0
daphne==4.0.0
Twisted[http2,tls]==23.8.0
```

#### there are other steps to make use of TLS

- make key: `openssl genrsa -out privatekey.pem 2048`

- make certificate `openssl req -new -x509 -key privatekey.pem -out cert.pem -days 365`

- run daphne with the keys: `daphne -b 0.0.0.0 -e ssl:8001:privateKey=privatekey.pem:certKey=cert.pem progress_app.asgi:application`
