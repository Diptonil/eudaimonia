# Eudaimonia
<div id="top"></div>
<span>
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" />
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" />
<img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white" />
<img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white">
<img src="https://img.shields.io/badge/Snyk-4C4A73?style=for-the-badge&logo=snyk&logoColor=white" />
<img src="https://img.shields.io/badge/Sentry-black?style=for-the-badge&logo=Sentry&logoColor=#362D59" />
<img src="https://img.shields.io/badge/Cloudinary-blue?style=for-the-badge&logo=Cloudways&logoColor=#2C39BD" />

</span>


## Table of Contents

- [Description](#description)
- [Frameworks and Tools](#frameworks-and-tools)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Tests](#tests)
- [Roadmap](#roadmap)
- [Credits](#credits)


## Description

Eudaimonia is a scalable and dynamic web application that serves to make journaling accessible to all, making it easy for users to inculcate a habit of periodic writing. The project highlights the benefits of journaling and regular usage of the application can be an enriching experience, which is facilitated by running ML models on the input data for scrutinizing their moods and creating reports on their behaviours. The main features of this project are:
<ul>
<li> Provides a secure environment for the user to log their daily activites, write about their feelings or monitor their daily activities.</li>
<li> Secures their data in the database using an AES-256 cryptographic algorithm.</li>
<li> Provides a sentiment analysis service using a Natural Language Processing model that processes the user's entry and provides music and film recommendations while also recording stats on their mental well-being.</li>
<li> Provides additional services such as customization of their writing panels, data recovery, etc.</li>
</ul>
The application was made with the intents of providing a market-ready service that can be utilized for personal development as well as providing features that other similar websites charge money for.
The future scole of the project would be to extend its use-cases, improving the UI significantly and adding in more features that provides the software a competitive edge over all existing products in the web.

<p align="right">(<a href="#top">Top</a>)</p>


## Frameworks and Tools

The major frameworks, tools, services and APIs used for the making of this project is hereby listed:

* [Django](https://www.djangoproject.com/): The fullstack framework used for building the web application.
* [PostgreSQL](https://www.postgresql.org/): The relational database used primarily.
* [RedisDB](https://redis.io/): The in-memory data store used for caching.
* [Selenium](https://www.selenium.dev): The browser automation framework used for validation testing.
* [Jira](https://www.atlassian.com/software/jira): The collaboration and software development tool used to simplify worflow.
* [Sentry](https://sentry.io/): The exception management service used for fatal error logging.
* [Snyk](https://snyk.io/): The security management service used for source code security vulnerability checks.
* [Cloudinary](https://cloudinary.com/): The primary file storage service.
* [Google SMTP](https://support.google.com/mail/answer/7126229?hl=en): The email server to send automated emails.
* [Whitenoise](http://whitenoise.evans.io/en/stable/): The web server used to fetch static files.
* [VSC](https://code.visualstudio.com/): The integrated IDE for development.

<p align="right">(<a href="#top">Top</a>)</p>


## Prerequisites

1. Install Python for your respective operating system at [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. Install version control system of Git for your respective operating system at [https://git-scm.com/downloads](https://git-scm.com/downloads).

<p align="right">(<a href="#top">Top</a>)</p>


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Diptonil/eudaimonia.git
    ```

2. Create a virtual environment for installation of required modules:
    ```sh
    python -m venv venv
    venv\scripts\activate
    pip install -r requirements.txt
    ```

3. Run the website on the development server:
    ```sh
    python manage.py runserver
    ```

Now the website is up and running (at port 8000 in case nothing else is mentioned). To access the website, go to http://localhost:8000/.

<p align="right">(<a href="#top">Top</a>)</p>


## Tests

The project has been developed with adherence to Test-Driven Development principles. Hence, there are a lot of tests that can be run to validate the requirements or verify the programming.<br>

To run Django verification tests:<br>
```sh
python manage.py test
```
We have Selenium integration for functional tests. A default webdriver is included with the repository. You can apply validation tests only if:
- A test period of around five minutes can be alloted for an interrupt-free functioning of the test suite.
- Google Chrome is the web browser being used.
- Sufficient memory resources can be allocated for the test execution (multiple instances of the same browser will be run simutaneously).
- 
To run Selenium validation tests:
```sh
python tests\scenario_testing.py
```

<p align="right">(<a href="#top">Top</a>)</p>


## Roadmap

There are subsequent upgrades to be made to the project to reach the final stage. Here are a list of all immediate objectives:

- [x] Configure initial particulars and services.
- [x] Develop authentication and authorization scheme.
- [x] Develop AES-256 encryption algorithm implementation.
- [ ] Implement the base theme of the website.
- [ ] Develop sentiment-analysis API.
- [ ] Develop frequency and habit analysis models.
- [ ] Deploy using CI/CD practices.

<p align="right">(<a href="#top">Top</a>)</p>


## Credits

The collaborators involved in this project are:

- Chaithanya S
- Diptonil Roy
- Divyansh Agrawal

The resources utilized for this project are:

- [Font Awesome](https://fontawesome.com)
- [Image Shields](https://shields.io)
- [Simple Icons](https://simpleicons.org/)
- [Datepicker](https://fengyuanchen.github.io/datepicker/)
- [Google reCaptcha](https://www.google.com/recaptcha/about/)
- [Argon2 Hashing Technique](https://argon2.online/)
- [AES-256 Encryption](https://www.nist.gov/publications/advanced-encryption-standard-aes)

<p align="right">(<a href="#top">Top</a>)</p>