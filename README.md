# mortgage-calc

**mortgage-calc** is a Django + vanilla async Javascript calculator to help potential home buyers understand whether it makes sense to buy a house. It is hosted at [MortgageROI.com](https://www.mortgageroi.com). 

Many mortgage calculators are overly simplistic, returning to the user a simple 'buy or rent' determination without any context (e.g., *why* is my return higher if I keep my home for 10 years v. 2 years? *why* does a higher down payment help in some cases and hurt in others? what is more important for my return, home appreciation or the rent I save?).

This calculator seeks to show the user a *return* and the *drivers of that return.*

Would love any feedback, pull requests, etc.

## Getting Started

*Requirements: Python 3*

Getting set up locally is simple. Once you've cloned the project: 

1) Run `pip install requirements.txt`
2) Set up a local_settings.py file and put drop it in the mortgage/ folder where the settings.py file lives

```python
# local_settings.py

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '[YOUR_SECRET_KEY]'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECURE_SSL_REDIRECT = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

3) Run `python3 manage.py migrate`

## Running the tests

My goal with this project is to have 100% test coverage server-side.

You may notice hard-coded values throughout the tests, e.g., `self.assertEqual(response_dict['base_irr'][30], 5.37)` -- since the final outcomes are reliant on so many calculations that would be tedious to recreate in tests, I've created a separate [Google Sheet](https://drive.google.com/open?id=1j4b3ZiP2LsMpawOkTHDcCzCRLOuV2KtaUuEGtLwS4E0) as a testing reference that contains the target outputs.

`coverage run --source='.' manage.py test` runs tests

`coverage html` generates the coverage files

## Built With

* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com/)
* [Chart.js](https://www.chartjs.org/) - Open source HTML5 charts


## Author

**Garrett Edel**
[LinkedIn](https://www.linkedin.com/in/garrettedel/)

## License

MIT License

Copyright (c) 2018 Garrett Edel

See [LICENSE.txt](LICENSE.txt) file for details
