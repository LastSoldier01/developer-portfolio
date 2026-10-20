# Developer Portfolio

A personal developer portfolio for a **junior backend developer (Python / Django)**, built with
Django Templates, HTML, CSS, and vanilla JavaScript. Projects, technologies, and cover images
are managed through the **Django Admin** — no hardcoded content.

## Design credit & attribution

The visual language, layout, and interaction design of this site are closely inspired by
**Brittany Chiang's [v4 portfolio](https://brittanychiang.com/)** (open-source at
[github.com/bchiang7/v4](https://github.com/bchiang7/v4), MIT license).

This design is not claimed as originally my own. Per the author's request, credit goes to
Brittany Chiang — go check out her work! The implementation here is an original
Django + server-rendered adaptation (no Gatsby/React/styled-components), with free font
substitutes (Inter, IBM Plex Mono) and content adapted to a Python/Django backend profile.

## Stack

- **Backend:** Python 3.14, Django 5.2 (LTS)
- **Frontend:** Django Templates, hand-written CSS, vanilla JS (IntersectionObserver)
- **Database:** SQLite (dev)
- **Dependency:** Pillow (for optional project cover images — required by Django's `ImageField`)

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Site: <http://127.0.0.1:8000/>
- Admin: <http://127.0.0.1:8000/admin/>
- Project archive: <http://127.0.0.1:8000/projects/>

## Customize (replace these placeholders)

| What | Where |
|---|---|
| Your name, email, social links | `config/site_config.py` (empty links are hidden automatically) |
| Your personal story paragraph | `templates/pages/home.html` (search for `Your story here`) |
| Your photo | Add a real image and replace the placeholder block in `templates/pages/home.html` |
| Technologies (skills list) | Django Admin → **Technologies** |
| Projects (featured + archive) | Django Admin → **Projects** (tick `Is featured` for the homepage showcase, `Is published` to go live) |

New projects are **drafts by default** (`Is published` unchecked) and return 404 until published.
Featured projects with no cover image show a styled "Preview coming soon" placeholder.

## Tests

```powershell
python manage.py check
python manage.py test
```

## License

Code in this repository is my own. The *design concept* belongs to
[Brittany Chiang](https://brittanychiang.com/).

