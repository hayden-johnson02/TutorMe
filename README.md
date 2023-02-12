# Django Practice Assessment


**Roles:**
- Anna Goco (aeg3dh): Requirements Manager
- Tyler Kim (tkj9ep): Scrum Master 
- Hayden Johnson (cxy6nx): Testing Manager
- Jade Gregoire (dze3jz): UX Designer
- Franklin Glance (fpg2kv): DevOps Manager


**Project Choice:** Tutor Me


**Heroku address:** https://project-a-03-tutorme.herokuapp.com/


## How to run locally:
Steps on MAC:
1. Clone this repository `gh repo clone uva-cs3240-s23/project-a-03`
2. Create virtual environment: `python -m venv env`
3. Activate env: `source env/bin/activate`
4. Install packages: `pip3 install -r requirements.txt`
5. Make migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Set up superuser: `python manage.py createsuperuser` 
7. Run development server: `python manage.py runserver`

Steps on Windows:
1. Clone this repository
2. Create virtual environment: `py -m venv env`
3. Activate env: `.\env\Scripts\activate`
4. Install packages: `py -m pip install -r requirements.txt`
5. Make migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Run development server: `py manage.py runserver`

To run locally `heroku local --port 8000` in the heroku cli
