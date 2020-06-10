# ar-content-platform-backend
![Build Status](https://travis-ci.com/thamidurm/ar-content-platform-backend.svg?branch=master)
[![codecov](https://codecov.io/gh/thamidurm/ar-content-platform-backend/branch/master/graph/badge.svg)](https://codecov.io/gh/thamidurm/ar-content-platform-backend)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/thamidurm/ar-content-platform-backend/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/thamidurm/ar-content-platform-backend/?branch=master)

This is the backend of the augmented reality platform created for the Semester 5 Software Engineering Project.

### Instructions for Running Locally

1. Install `python 3.7.6` or higher
2. Run `python -m venv /path/to/new/virtual/environment` to create an isolated python environment
3. Run `path/to/new/virtual/environment/Scripts/activate` to start the isolated environment
4. Change the directory to the root of the cloned project and run `pip install -r requirements.txt` in the isolated environment 
5. Run `python manage.py runserver` to start the development server
6. Run `python manage.py test` to run the tests
