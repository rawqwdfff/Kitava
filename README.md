                                                  Kitava


### Installation:

Requirements:

- Python 3 runtime
- Django==3.2.6
- django-crispy-forms==1.12.0

- Other dependencies in `requirements_personal.txt`

To Setup the repo locally:

Follow these steps:

```
git clone https://github.com/rawqwdfff/Kitava.git
```

Make sure you have python 3 and pipenv installed on your pc.

Then follow these steps:

```
cd <project-directory>
```

```
pipenv install --dev
```

- Activate the new virtual environment:

```
pipenv shell
```

- cd into project:

```
cd Kitava/
```

- Make database migrations:

```
python manage.py makemigrations

python manage.py migrate
```

- Create a superuser

```
python manage.py createsuperuser
```

- Run development server on localhost

```
python manage.py runserver
```
