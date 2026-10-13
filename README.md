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

##  Default Admin Credentials

After running `python manage.py seed_data`:
- **Username**: `admin`
- **Password**: `adminpassword123`
- **Email**: `admin@nexus.local`
