# SkillForge Hub

SkillForge Hub is a Django-based learning platform where instructors publish courses and lessons while students enroll, follow curated content, and track their own progress. The stack is production-ready (Docker, Postgres, Redis, nginx, certbot) but still easy to run locally for day-to-day development.

---

## ✨ Highlights
- **Two roles**: instructors build courses/lessons; students enroll and consume content.
- **Role-aware dashboards**: tailored entry points after login.
- **Lesson media support**: text + embedded video links.
- **Secure access control**: only enrolled students can see private lessons; instructors can edit only their own material.
- **12-factor friendly**: configuration via `.env`, stateless web container, Redis-backed cache/session layer, PostgreSQL for persistence.

---

## 🧱 Architecture
| Layer | Tech | Notes |
| --- | --- | --- |
| Web | Django + Gunicorn | lives in `LearningPlatform/` + apps (`users`, `courses`, `enrollments`). |
| DB | PostgreSQL 15 | mounted volume `postgres_data`. |
| Cache/Sessions | Redis 7 | optional fallback to DB sessions for dev. |
| Reverse proxy | nginx (Docker) | SSL termination, static/media serving, proxy to Gunicorn. |
| Certificates | certbot / self-signed | self-signed for local, Let's Encrypt for prod via `setup-ssl-certificates.sh`. |

Project layout (top-level):
```
LearningPlatform/     Django project + settings
courses/, users/, enrollments/   Domain apps
nginx/               nginx.conf + TLS assets
start.sh, check-status.sh, setup-ssl-certificates.sh
Dockerfile, docker-compose.yml
```

---

## 🧑‍💻 Local Development (venv + SQLite)
Prereqs: Python 3.12+, pip, virtualenv.

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # create one if missing, point to dev settings
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000 and log in with the superuser. Instructor/student profiles can be toggled from the admin (`/admin`).

---

## 🐳 Full Stack via Docker Compose
Use this path when you want Postgres, Redis, and nginx locally (mirrors prod).

```bash
./start.sh
```
The helper script stops host nginx, frees ports 80/443, rebuilds the `web` image, starts the compose stack, waits for health checks, and prints container status. Static files are collected automatically inside the `web` container before Gunicorn starts.

Monitor everything with:
```bash
./check-status.sh
```
This reports container health, bound ports, HTTP(S) probes, and tail logs for each service.

Bring everything down when you are done:
```bash
docker compose down
```

---

## 🔐 HTTPS & Domains
- Local self-signed certs live under `nginx/ssl/skillshare.local.*` (browsers will warn—accept once).
- For a real domain (e.g., `skillforge.bg`), point DNS A records to your server, then run:
```bash
sudo ./setup-ssl-certificates.sh skillforge.bg admin@skillforge.bg
```
This installs certbot, issues Let’s Encrypt certificates, wires them into nginx, restarts containers, and schedules auto-renewals.

---

## 🧪 Tests
```bash
python manage.py test
```
Tests cover authentication flows, course CRUD, lesson visibility, and enrollment logic. Run them inside the virtualenv or with `docker compose exec web python manage.py test`.

---

## 📂 Environment Variables
Key variables pulled from `.env` (see `LearningPlatform/settings/base.py`):
- `DJANGO_SETTINGS_MODULE` – `LearningPlatform.settings.dev` or `.prod`
- `SECRET_KEY` – required for any deployment
- `DEBUG` – `True` locally, `False` in prod
- `DB_*` – Postgres credentials/host/port
- `REDIS_URL` – e.g., `redis://redis:6379/1`
- `ALLOWED_HOSTS` – comma-separated hostnames (`localhost,skillforge.bg,...`)

---

## 🧰 Utility Scripts
| Script | Purpose |
| --- | --- |
| `start.sh` | Full clean start: stops conflicting services, rebuilds containers, waits for health checks. |
| `check-status.sh` | Summarizes container health, listening ports, HTTP(S) probes, log tails. |
| `setup-ssl-certificates.sh` | Automates certbot issuance and nginx reload for real domains. |

---

## 🚀 Deployment Flow
1. Provision server (Ubuntu 22.04+, Docker + Compose installed).
2. Clone repo + configure `.env` with production secrets/hosts.
3. Point DNS (e.g., `skillforge.bg`, `www.skillforge.bg`) to server IP.
4. Run `sudo ./setup-ssl-certificates.sh skillforge.bg admin@skillforge.bg`.
5. Launch services: `./start.sh` (or `docker compose up -d`).
6. Create admin user: `docker compose exec web python manage.py createsuperuser`.
7. Monitor with `./check-status.sh` and `docker compose logs -f`.

With these steps your SkillForge Hub instance is ready for instructors and students worldwide. Happy teaching & learning! 🧠✨
