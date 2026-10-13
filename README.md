# Nexus Headless CMS

A decoupled, high-craft content management system built with **Django**, **Django REST Framework (DRF)**, **SQLite**, and a consumer-facing reading frontend.

---

## 🎨 Editorial Design System

- **Primary Background**: Warm Beige (`#F9F6F0`)
- **Cards & Surfaces**: Soft White (`#FFFFFF`) with subtle border (`#E6E0D4`) and paper elevation (`0 4px 12px rgba(44, 40, 37, 0.05)`)
- **Primary Accent**: Terracotta (`#C85A32`)
- **Tags & Badges**: Sage Green (`#6B8E7B`)
- **Body Typography**: Deep Charcoal / Espresso (`#2C2825`), Playfair Display & Plus Jakarta Sans

---

## 🚀 Quickstart for Other Developers (Running Locally)

Anyone who clones this repository can get the UI and API running locally in 4 simple commands:

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/nexus-cms-api.git
cd nexus-cms-api

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Seed database with superuser and sample articles
python manage.py seed_data

# 5. Start the development server
python manage.py runserver
```

Once running, visit:
- **Reader Publication UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Editorial Admin Desk**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **REST API Articles**: [http://127.0.0.1:8000/api/articles/](http://127.0.0.1:8000/api/articles/)
- **REST API Categories**: [http://127.0.0.1:8000/api/categories/](http://127.0.0.1:8000/api/categories/)

---

## 🔑 Default Admin Credentials

After running `python manage.py seed_data`:
- **Username**: `admin`
- **Password**: `adminpassword123`
- **Email**: `admin@nexus.local`

---

## 🌐 Deploying Online (No Local Setup Required for Viewers)

If you want people to view the UI directly in their browser without downloading code or running commands:
1. Push this repository to GitHub.
2. Connect it to a hosting platform like **Render** ([render.com](https://render.com)) or **Railway** ([railway.app](https://railway.app)).
3. Set the build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data`
4. Set the start command: `python manage.py runserver 0.0.0.0:$PORT` (or `gunicorn config.wsgi`)
5. Share the live public URL!
