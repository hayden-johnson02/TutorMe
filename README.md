# Django Practice Assessment


**Roles:**
- Anna Goco (aeg3dh): Requirements Manager
- Tyler Kim (tkj9ep): Scrum Master 
- Hayden Johnson (cxy6nx): Testing Manager
- Jade Gregoire (dze3jz): UX Designer
- Franklin Glance (fpg2kv): DevOps Manager


**Project Choice:** Tutor Me


**Heroku address:** https://project-a-03-tutorme.herokuapp.com/

For local development, run export DJANGO_DEVELOPMENT=true, or add export DJANGO_DEVELOPMENT=true to .bashrc file

## How to run locally:
**On MAC:**
1. Clone this repository `gh repo clone uva-cs3240-s23/project-a-03`
2. Create virtual environment: `python3 -m venv .venv`
3. Activate env: `source .venv/bin/activate`
4. Install packages: `pip3 install -r requirements.txt`
5. Make migrations: `python3 manage.py makemigrations` and `python3 manage.py migrate`
6. Set up superuser: `python3 manage.py createsuperuser` 
7. Run `export DJANGO_DEVELOPMENT=true`
8. To run server locally: `python manage.py runserver`
(Run heroku locally: `heroku local --port 8000`, may need to run `python manage.py collectstatic` first) 

**On Windows:**
1. Clone this repository
2. Create virtual environment: `py -m venv env`
3. Activate env: `.\env\Scripts\activate`
4. Install packages: `py -m pip install -r requirements.txt`
5. Make migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Run `set DJANGO_DEVELOPMENT=true`
7. To run server locally: `python manage.py runserver`
(To run heroku locally: `heroku local -f Procfile.windows`, may need to run `python manage.py collectstatic` first) 

To run locally `heroku local --port 8000` in the heroku cli


**Notes:**
- `heroku git:remote -a project-a-03-tutorme` to set heroku remote