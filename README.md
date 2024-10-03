# Django channels socket example app

#### setup and install
install poetry if it is not installed and run `poetry install`


#### migrate

`python manage.py migrate`

#### run

`daphne -b 0.0.0.0 -p 8001 progress_app.asgi:application`

#### open

[http://localhost:8001/](http://localhost:8001/)

#### see

![Browser](/browser.png)

### [code snippets](/deets.md)
