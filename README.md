# Steel Horse Group — Django website

Hot shot courier & oilfield freight site, built from the Steel Horse Group landing page design.

## What's included

- One-page site: masthead, hero with dispatch status card, services, coverage map of cities, fleet illustration, why-us list, footer.
- **Pickup request form** that saves to the database (with a spam honeypot) and optionally emails dispatch.
- **Django admin** (`/admin/`) to edit everything without touching code:
  - *Site settings* — company name, phone, email, base city, NSC/CVOR number, accent colour
  - *Services*, *Service areas*, *Why-us points* — add, reorder, hide
  - *Pickup requests* — search, filter, and move through New → Quoted → Booked → Delivered
- Starting content is loaded automatically by migration `0002_seed_content`.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 for the site and http://127.0.0.1:8000/admin/ for the admin.
First thing: go to **Admin → Site settings** and replace the `[PHONE NUMBER]`, `[CITY]` and `[NSC / CVOR NUMBER]` placeholders.

Run the tests with `python manage.py test`.

## Settings (environment variables)

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Secret key — **set this in production** | dev key |
| `DJANGO_DEBUG` | `1` for dev, `0` for production | `1` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated domains | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | e.g. `https://steelhorsegroup.ca` | empty |
| `DISPATCH_EMAIL` | Where new pickup requests are emailed | empty (no email) |
| `DJANGO_EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | SMTP settings | console backend |

## Deploying

For production: set `DJANGO_DEBUG=0`, a real `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`, run
`python manage.py collectstatic`, and serve with a WSGI server such as gunicorn
(`pip install gunicorn`, then `gunicorn steelhorse.wsgi`). Hosts like Render, Railway or PythonAnywhere
work well; for static files there, add `whitenoise`.
