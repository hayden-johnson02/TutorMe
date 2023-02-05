# Django Practice Assessment


**Roles:**
- Anna Goco (aeg3dh): Requirements Manager
- Tyler Kim (tkj9ep): Scrum Master 
- Hayden Johnson (cxy6nx): Testing Manager
- Jade Gregoire (dze3jz): UX Designer
- Franklin Glance (fpg2kv): DevOps Manager


**Project Choice:** Tutor Me


**Heroku address:** https://project-a-03-tutorme.herokuapp.com/

Git: https://git.heroku.com/project-a-03-tutorme.git


## How to run locally:
1. Clone this repository `gh repo clone uva-cs3240-s23/project-a-03`
2. Create virtual environment: `python -m venv env`
3. Activate env: `source env/bin/activate`
4. Install packages: `pip3 install -r requirements.txt`
5. Make migrations: `python manage.py makemigrations` and `python manage.py migrate`
6. Set up superuser: `python manage.py createsuperuser` 
7. Run development server: `python manage.py runserver`


To test heroku locally run `heroku local --port 8000` in the heroku cli
