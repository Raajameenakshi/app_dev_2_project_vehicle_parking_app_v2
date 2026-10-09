# Modern Application Development 2 Project - Vehicle Parking App V2

A multi-user web application for managing 4-wheeler parking lots, spots, and bookings. Built as the project for Modern Application Development II (MAD II).

Admins create and manage parking lots and spots. Users book a spot, release it when they leave, and track their parking history and spending. Background jobs handle reminders, monthly reports, and CSV exports.

**Demo video:** [Watch on Google Drive](https://drive.google.com/file/d/1E3MX7AwIBAKyEhMR20JI1XAoldGSmSdA/view?usp=sharing)

## Features

### Admin
- Log in with role-based access (a single admin account is created automatically when the database is first created)
- Create, edit, and delete parking lots (a lot can be deleted only when its spots are empty)
- Spots are generated automatically from the lot's maximum number of spots
- View each spot's status and the booking details of occupied spots
- Mark a free spot as unavailable (for example, for maintenance) and make it available again
- View all registered users and all bookings
- View summary charts for revenue per lot and spot occupancy

### User
- Register and log in
- Browse available parking lots and book a spot (the app allots the next free spot)
- Release the spot when leaving; the cost is calculated from the parking duration
- View booking history and spending summaries (monthly and per lot)
- Export booking history as a CSV file (runs as a background job)

### Background Jobs (Celery + Redis)
- **Daily reminder** sent to users through a Google Chat webhook
- **Monthly activity report** sent to users by email as HTML
- **CSV export** triggered by the user, processed asynchronously

### Performance
- Redis caching with expiry on frequently used endpoints (user list, available lots)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask, Flask-SQLAlchemy |
| Frontend | Vue 3, Vue Router, Pinia, Chart.js |
| Database | SQLite |
| Authentication | JWT (Flask-JWT-Extended), password hashing with Werkzeug |
| Caching | Redis, Flask-Caching |
| Background jobs | Celery, Celery Beat, Redis |
| Email | SMTP (Flask-side `smtplib`) |

## Database Schema

- **Admin**: id, email, password (hashed)
- **User**: id, email, password hash, full name, address, pincode
- **Parking_lot**: id, location, address, pincode, price, max_no_spots, landmark
- **Parking_spot**: id, parking_lot_id (FK), is_booked, additional_info
- **Booking**: id, user_id (FK), parking_spot_id (FK), vehicle_number, start_time, end_time, cost

## API Overview

| Group | Purpose | Example endpoints |
|---|---|---|
| Auth | Register, login, logout (JWT) | `/api/register`, `/api/login`, `/api/logout` |
| Admin | Manage lots, spots, users, bookings, summary | `/api/admin/parking-lots`, `/api/admin/summary` |
| User | Browse lots, book, release, bookings, summary | `/api/user/available_lots`, `/api/user/reserve` |
| Export | Start a CSV export and fetch its result | `/api/export-csv`, `/api/csv_result/<task_id>` |

## Project Structure

    Vehicle-Parking-App-V2/
    ├── backend/
    │   ├── app.py                 # Flask app, config, Celery Beat schedule
    │   ├── applications/
    │   │   ├── models.py          # Database models
    │   │   ├── routes.py          # API routes (auth, admin, user, export)
    │   │   ├── tasks.py           # Celery jobs (reminders, reports, CSV)
    │   │   ├── mail.py            # Email sending
    │   │   ├── celery_init.py     # Celery setup
    │   │   ├── celery_config.py   # Broker and result backend settings
    │   │   └── cache_instance.py  # Cache setup
    │   └── static/                # Generated CSV exports
    ├── frontend/
    │   └── src/
    │       ├── router/            # Vue Router
    │       ├── components/        # Headers and charts
    │       └── views/
    │           ├── admin/         # Admin pages
    │           ├── user/          # User pages
    │           └── Auth/          # Login and register
    ├── instance/                  # SQLite database
    └── requirements.txt

