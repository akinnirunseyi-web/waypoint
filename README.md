# Waypoint

A trail-finder and trip-planner built with Python and Django.  
Course: CCGC-5003 Application Programming — Summer 2026  
Student: Akinnirun Oluwaseyi (N10009815)

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/akinnirunseyi-web/waypoint.git
cd waypoint
```

**2. Create and activate virtual environment**
```bash
python3 -m venv env
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run migrations**
```bash
python3 manage.py migrate
```

**5. Start the server**
```bash
python3 manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000**

### Admin access
Create a superuser to manage trails via the admin panel:
```bash
python3 manage.py createsuperuser
```
Then go to: **http://127.0.0.1:8000/admin/**

---

## Pages

| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/catalog/` | Trail catalog (from database) |
| `/trails/parks/` | Browse all parks |
| `/trails/parks/<id>/` | Trails in a specific park |
| `/report/` | Report a trail form |
| `/search/` | Search trails |
| `/admin/` | Admin panel (superuser only) |

---

## MVT Pattern

Django follows the MVT (Model-View-Template) pattern:

- Model — defines the data and talks to the database
- View — contains the logic; receives a request and returns a response  
- Template — the HTML that presents data to the user

The request flow is:
Browser → URL → View → Model (if needed) → Template → Browser

## Project Structure

waypoint_core/ — Pure Python domain engine (Weeks 7-8)
waypoint/ — Django project settings folder
manage.py — Django command-line tool
requirements.txt — Pinned dependencies
.gitignore — Excludes env/, db.sqlite3, pycache

## Data Model

- **Park** — name, region
- **Trail** — name, distance_km, elevation_gain, difficulty, is_open, added
- **Relationship** — each Trail belongs to a Park via ForeignKey (SET_NULL)
  - Deleting a park does not delete its trails
  - Trails can exist without a park (null=True)