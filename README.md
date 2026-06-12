# ARPBIG IdISBa — Antimicrobial Resistance Database

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-reverse--proxy-009639?logo=nginx&logoColor=white)
![License](https://img.shields.io/badge/license-All%20rights%20reserved-lightgrey)

A Django web application for storing, querying and analysing antimicrobial
resistance (AMR) data of bacterial isolates — primarily *Pseudomonas
aeruginosa* — at the Institut d'Investigació Sanitària Illes Balears (IdISBa).

It manages isolate metadata, MIC values with dynamic S/I/R clinical
categorisation, the mutational and acquired resistome, sequencing information
and a physical strain bank, with role-based access control and an interactive
resistome heatmap.

---

## Table of Contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Architecture](#architecture)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Running the app](#running-the-app)
- [User roles](#user-roles)
- [Project structure](#project-structure)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Advanced search** across isolate metadata, clinical data, phenotype and
  genotype, combining multiple filters simultaneously.
- **MIC table** for 35+ antibiotics with **dynamic S/I/R clinical
  categorisation** based on configurable breakpoint tables (EUCAST, CLSI or
  custom versions).
- **Resistome heatmap** — interactive Plotly visualisation of mutations and
  polymorphisms per gene and isolate.
- **Bulk data upload** from Excel/CSV through a guided column-mapping wizard.
- **Strain bank** management with freezer / rack / box / position views.
- **Statistics dashboard** powered by Plotly Dash (sequence type distribution,
  geographic map, and more).
- **Flexible data export** to CSV, Excel and TXT, with configurable presets.
- **Role-based access control** with three profiles: Administrator, Editor and
  Guest.

---

## Tech stack

| Layer            | Technology                                                        |
|------------------|-------------------------------------------------------------------|
| Backend          | Python 3.10, Django 4.2                                            |
| Database         | MySQL 8 (InnoDB, utf8mb4)                                          |
| WSGI server      | Gunicorn                                                           |
| Reverse proxy    | Nginx                                                              |
| Env management   | Pipenv (Pipfile / Pipfile.lock)                                    |
| Key Django libs  | django-tables2, django-filter, django-crispy-forms, django-import-export, django-advanced-filters, django-plotly-dash |
| Visualisation    | Plotly / Plotly Dash                                               |
| Frontend         | Bootstrap 4, Select2, W3.CSS                                       |

---

## Architecture

```
Browser (HTTPS)
      │
    Nginx ──── /static/  →  served directly from STATIC_ROOT
      │
   Gunicorn  (Unix socket)
      │  WSGI
   Django  →  LoginRequiredMiddleware (RBAC)  →  Views  →  ORM
      │
   MySQL 8
```

A detailed architecture diagram is available in
[`Documentation/`](Documentation/).

---

## Getting started

### Prerequisites

- Python 3.10
- MySQL 8 (running locally or reachable remotely)
- Pipenv (`pip install pipenv`)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<owner>/ARPBIGIDISBA_docker.git
cd ARPBIGIDISBA_docker

# 2. Install dependencies in an isolated environment
pipenv install
pipenv shell

# 3. Configure environment variables (see Configuration below)
cp .env.example .env
#    edit .env with your own values

# 4. Apply database migrations
cd ARPBIGIDISBA_frontend
python manage.py migrate

# 5. Create the user groups (Editor, Guest)
python manage.py loaddata home/fixtures/initial_groups.json

# 6. Create an administrator account
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput
```

---

## Configuration

The application is configured through environment variables loaded from a
`.env` file. **Never commit your `.env` file** — only `.env.example` belongs in
version control.

| Variable             | Description                                  |
|----------------------|----------------------------------------------|
| `DJANGO_SECRET_KEY`  | Django secret key (unique per environment)   |
| `DEBUG`              | `True` for development, `False` in production |
| `DB_HOST`            | MySQL host                                   |
| `DB_PORT`            | MySQL port (default `3306`)                  |
| `MYSQL_DATABASE`     | Database name                                |
| `MYSQL_USER`         | Database user                                |
| `MYSQL_PASSWORD`     | Database password                            |

Generate a fresh secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Running the app

### Development

```bash
cd ARPBIGIDISBA_frontend
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

### Production

In production the app is served by Gunicorn behind Nginx. See
[Deployment](#deployment).

---

## User roles

Access is controlled by `home/middleware.py` (`LoginRequiredMiddleware`) and
the `home.context_processors.user_role` context processor. Three profiles are
defined:

| Profile        | Django group | `is_staff` | `is_superuser` | Access                                             |
|----------------|--------------|:----------:|:--------------:|----------------------------------------------------|
| **Guest**      | `Invitado`   | No         | No             | Read-only: search, results, exports, dashboards    |
| **Editor**     | `Editor`     | No         | No             | All views, including data upload and strain editing |
| **Administrator** | —         | Yes        | Yes            | Full access, including the Django admin panel       |

Routes requiring Editor privileges are listed in `EDITOR_REQUIRED_PATHS` in
`settings.py`. Denied access attempts are logged to `logs/access_denied.log`.

---

## Project structure

```
ARPBIGIDISBA_docker/
├── ARPBIGIDISBA_frontend/      # Django project
│   ├── ARPBIGIDISBA_frontend/  # settings, urls, wsgi, asgi
│   ├── home/                   # core app: models, views, admin, middleware, RBAC
│   ├── upload/                 # bulk data-upload wizard
│   ├── bank/                   # strain bank management
│   ├── dashboard/              # Plotly Dash visualisations
│   ├── apps/                   # additional bioinformatics tools
│   └── manage.py
├── Documentation/              # manuals and ER diagrams
├── SourceFiles/                # additional source files
├── logs/                       # application logs (gitignored)
├── gunicorn_config.py          # Gunicorn configuration
├── Pipfile / Pipfile.lock      # dependency management
└── .env.example                # environment-variable template
```

---

## Deployment

Production runs two environments — **PRE-production** and **production** — each
updated via a dedicated git-pull script. The high-level update procedure is:

```bash
# 1. Pull the latest code (runs as www-data)
sudo bash /var/www/arpbig_db/scripts/update-arpbig_predb-git.sh   # PRE
# or update-arpbig_db-git.sh for production

# 2. Apply post-update steps
cd <project>/ARPBIGIDISBA_frontend
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

Full deployment, backup/restore, monitoring and troubleshooting instructions
are in the **Technical Manual** under [`Documentation/`](Documentation/).

---

## Documentation

| Document            | Audience       | Contents                                              |
|---------------------|----------------|-------------------------------------------------------|
| **User Manual**     | Researchers    | Step-by-step guide to every screen and feature        |
| **Technical Manual**| Administrators | Architecture, database schema, RBAC, deployment, ops  |
| **ER diagrams**     | Developers     | Entity-relationship diagrams (draw.io, editable)      |

All documents live in the [`Documentation/`](Documentation/) directory.

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository and create a feature branch
   (`git checkout -b feature/my-change`).
2. Follow the existing code style; keep code and comments in English.
3. Make sure migrations are included when models change.
4. Open a pull request describing the change and its motivation.

For larger changes, please open an issue first to discuss what you would like
to change.

---

## License

No license has been specified yet. Until a license is added, this code is
**all rights reserved** by its authors. Please contact the maintainers before
reusing it.

---

## Acknowledgements

Developed by the **ARPBIG** research group
([arpbigidisba.com](https://arpbigidisba.com)) at the Institut d'Investigació
Sanitària Illes Balears (IdISBa), in collaboration with Hospital Universitari
Son Espases.
