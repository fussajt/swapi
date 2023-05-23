STAR WARS API EXPLORER
======================

Project overview:
- Django project settings are placed in `swapi` folder.
- Web application logic is placed in `web` folder.
- To install dependencies run: `pip install -r requirements.txt`
- To install dev dependencies run: `pip install -r requirements_dev.txt`
- Tests are run by pytest. To execute type: `pytest`
- To run the application on local machine in development mode type: `./manage.py runserver`


TODO:
-----
- Fix django test settings. Right now it uses `*` to import settings from base file. Also we need separate settings for production.
- Improve presentation layer. Right now it is minimal. It should be more user friendly with dynamic content loading, loaders indicators, etc.
- For simplicity we generate collection table as html code from `petl`. With improved UI we probably should use `json` format passed to frontend.
- Add search and sort functionality to collection set.
- Dockerize.
