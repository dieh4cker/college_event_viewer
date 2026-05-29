# College Event Viewer

A Flask-based college event management web application for Government Polytechnic Hamirpur. The app lets students view notices, browse athletic and sports events, register for events, submit contact queries, and access college information pages. It also includes an admin panel for managing notices, events, registrations, contacts, dashboards, CSV imports, and PDF exports.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Database](#database)
- [Admin Access](#admin-access)
- [Public Pages](#public-pages)
- [Admin Pages](#admin-pages)
- [CSV Upload Format](#csv-upload-format)
- [PDF Export](#pdf-export)
- [Static Assets and Scripts](#static-assets-and-scripts)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)
- [Future Improvements](#future-improvements)

## Features

### Student/Public Features

- Home page with important notices.
- Athletic event listing with event name, date, time, and judges.
- Sports event listing with event name, date, time, and judges.
- Event registration form for athletic and sports events.
- Multiple event selection using checkboxes.
- Contact form for student queries.
- About page.
- Examination page.
- Studies and admission page with interactive trade and semester sections.
- Responsive sidebar navigation for desktop and mobile screens.

### Admin Features

- Admin login and logout.
- Admin dashboard with:
  - Total participant count.
  - Total athletic event count.
  - Total sports event count.
  - Participants-per-game chart.
  - Branch-wise participation chart.
- Add athletic events manually.
- Upload athletic events from CSV.
- Delete athletic events.
- Add sports events manually.
- Upload sports events from CSV.
- Delete sports events.
- Create notices.
- Delete notices.
- View registered students.
- Filter registered students by selected event.
- Download filtered participant lists as PDF.
- Clear all registrations.
- View contact queries.
- Delete contact queries.
- Register additional admin users.

## Tech Stack

- Backend: Flask
- Database ORM: Flask-SQLAlchemy / SQLAlchemy
- Database: SQLite
- Templates: Jinja2 HTML templates
- Frontend: HTML, CSS, JavaScript
- Charts: Chart.js loaded from CDN
- PDF generation: ReportLab
- Runtime language: Python

## Project Structure

```text
college_event_viewer/
|-- main.py
|-- requirements.txt
|-- athletic.csv
|-- sports.csv
|-- README.md
|-- instance/
|   `-- database.db
|-- static/
|   |-- Style.css
|   |-- admin.css
|   |-- login.css
|   |-- images/
|   |   `-- college.jpg.avif
|   `-- js/
|       |-- graph.js
|       |-- pdfdata.js
|       |-- registerFilter.js
|       `-- studyAdmission.js
`-- templates/
    |-- about.html
    |-- admin-login.html
    |-- admin.html
    |-- adminBase.html
    |-- athletic-manage.html
    |-- athletic.html
    |-- clientBase.html
    |-- contact.html
    |-- delete-event.html
    |-- deletenotice.html
    |-- deleteSportsEvent.html
    |-- examination.html
    |-- index.html
    |-- manage-contact.html
    |-- notice.html
    |-- registration-manage.html
    |-- registration.html
    |-- rigester-admin.html
    |-- sports-manage.html
    |-- sports.html
    `-- studies&admission.html
```

## Requirements

- Python 3.10 or newer is recommended.
- `pip`
- A modern web browser.
- Internet access while using the admin dashboard, because Chart.js is loaded from a CDN.

Python packages are listed in `requirements.txt`:

```text
Flask
Flask-SQLAlchemy
SQLAlchemy
reportlab
pillow
Werkzeug
Jinja2
```

The exact pinned versions are stored in the requirements file.

## Installation

Clone or open the project folder:

```bash
cd college_event_viewer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate the virtual environment on Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

Start the Flask app:

```bash
python main.py
```

By default, the app runs on:

```text
http://localhost:5000
```

The app is configured in `main.py` to run with:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

This means it listens on all network interfaces while running locally. In development, you can open it from the same machine using `http://127.0.0.1:5000` or `http://localhost:5000`.

## Database

The project uses SQLite through Flask-SQLAlchemy.

Database configuration:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
```

Because this is a Flask instance-relative SQLite URI, the database is stored at:

```text
instance/database.db
```

When `main.py` starts, it runs:

```python
with app.app_context():
    db.create_all()
```

This creates missing tables automatically.

### Database Tables

The application defines these models in `main.py`:

| Model | Table | Purpose |
| --- | --- | --- |
| `Admin` | `admin` | Stores admin login users. |
| `Notice` | `notice` | Stores notices shown on the home page. |
| `Athletic` | `athletic` | Stores athletic events. |
| `Sports` | `sports` | Stores sports events. |
| `Contact` | `contact` | Stores contact form messages. |
| `GamesRegister` | `games_register` | Stores student event registrations. |

### Model Fields

`Admin`

- `id`
- `name`
- `email`
- `passwd`

`Notice`

- `sno`
- `title`
- `desc`

`Athletic`

- `id`
- `eventName`
- `date`
- `time`
- `judges`

`Sports`

- `id`
- `eventName`
- `date`
- `time`
- `judges`

`Contact`

- `sno`
- `name`
- `email`
- `message`

`GamesRegister`

- `id`
- `name`
- `branch`
- `semester`
- `email`
- `phone`
- `sbrn`
- `game`
- `event_type`

## Admin Access

Admin login page:

```text
/admin-login
```

After successful login, the admin is redirected to:

```text
/admin
```

The admin session key is:

```python
session['admin']
```

Most admin routes check for this session value and redirect unauthenticated users back to `/admin-login`.

### First Admin User

The route for creating additional admins is:

```text
/register-admin
```

However, this route is protected and requires an existing admin session. If the bundled `instance/database.db` already contains an admin user, log in with that user first and then create more admins from the admin panel.

If you start with an empty database, you must insert the first admin manually using a database browser, SQLite tool, or a short Flask shell/script. The `admin` table requires:

```text
name, email, passwd
```

Example SQL:

```sql
INSERT INTO admin (name, email, passwd)
VALUES ('Admin', 'admin@example.com', 'admin123');
```

After that, visit `/admin-login` and sign in with the inserted email and password.

## Public Pages

| Route | Methods | Template | Description |
| --- | --- | --- | --- |
| `/` | GET | `index.html` | Home page with notices and college introduction. |
| `/athletic` | GET | `athletic.html` | Lists athletic events. |
| `/sports` | GET | `sports.html` | Lists sports events. |
| `/examination` | GET | `examination.html` | Examination page. |
| `/about` | GET | `about.html` | About page. |
| `/study-admission` | GET | `studies&admission.html` | Studies and admission page. |
| `/event-register?type=athletic` | GET, POST | `registration.html` | Registration form for athletic events. |
| `/event-register?type=sports` | GET, POST | `registration.html` | Registration form for sports events. |
| `/contact` | GET, POST | `contact.html` | Contact form. |

### Event Registration

The event registration page uses the `type` query parameter:

```text
/event-register?type=athletic
/event-register?type=sports
```

When the type is `athletic`, the form loads events from the `Athletic` table. When the type is `sports`, it loads events from the `Sports` table.

Submitted registrations are saved in the `GamesRegister` table.

Registration fields:

- Full name
- Branch
- Semester
- Email
- Phone number
- SBRN number
- Selected games/events
- Event type

## Admin Pages

| Route | Methods | Template | Description |
| --- | --- | --- | --- |
| `/admin-login` | GET, POST | `admin-login.html` | Admin login page. |
| `/admin` | GET | `admin.html` | Dashboard with counts and charts. |
| `/register-admin` | GET, POST | `rigester-admin.html` | Add a new admin user. |
| `/logout` | GET | None | Logs out the current admin. |
| `/manage-athletic` | GET, POST | `athletic-manage.html` | Add or upload athletic events. |
| `/delete-event` | GET | `delete-event.html` | View athletic events for deletion. |
| `/delete-event/<id>` | GET, POST | None | Delete one athletic event. |
| `/manage-sports` | GET, POST | `sports-manage.html` | Add or upload sports events. |
| `/delete-sports-event` | GET | `deleteSportsEvent.html` | View sports events for deletion. |
| `/delete-sports-event/<id>` | GET, POST | None | Delete one sports event. |
| `/notice` | GET, POST | `notice.html` | Create notices. |
| `/delete-notice` | GET | `deletenotice.html` | View notices for deletion. |
| `/delete-notice/<id>` | GET, POST | None | Delete one notice. |
| `/manage-registered` | GET | `registration-manage.html` | View and filter registered students. |
| `/download-filtered-pdf` | POST | None | Generate filtered participant PDF. |
| `/clear-registrations` | POST | None | Delete all registrations. |
| `/manage-contact` | GET | `manage-contact.html` | View contact messages. |
| `/delete-contact/<id>` | GET, POST | None | Delete one contact message. |

## CSV Upload Format

Admins can upload CSV files for both athletic and sports events.

Sample files are included:

- `athletic.csv`
- `sports.csv`

Required CSV header:

```csv
eventName,date,time,judges
```

Example:

```csv
eventName,date,time,judges
100m Sprint,2026-02-21,09:30,"Mr Sharma, Rahul Sharma"
Long Jump,2026-02-22,09:30,"Mr Verma, Suresh Kumar"
```

### CSV Column Rules

- `eventName`: Event name shown to students.
- `date`: Must use `YYYY-MM-DD` format.
- `time`: Must use 24-hour `HH:MM` format.
- `judges`: Can contain multiple names separated by commas. If commas are used, wrap the value in quotes.

Correct:

```csv
Cricket Match,2026-02-21,09:00,"Mr Sharma, Rahul Verma"
```

Incorrect:

```csv
Cricket Match,21-02-2026,9 AM,Mr Sharma, Rahul Verma
```

The app formats dates as `DD-MM-YYYY` and times as `HH:MM AM/PM` when displaying events.

## PDF Export

The registered students page includes a game filter and a PDF download button.

Flow:

1. Admin opens `/manage-registered`.
2. Admin selects a game from the dropdown.
3. JavaScript filters the visible table rows.
4. Admin clicks `Download PDF`.
5. `static/js/pdfdata.js` sends visible rows to `/download-filtered-pdf`.
6. Flask uses ReportLab to generate a PDF.
7. The browser downloads the file as:

```text
<selected-game>_participants.pdf
```

The generated PDF includes:

- Title
- Name
- Branch
- Semester
- Email
- Phone
- Game
- Total participant count

## Static Assets and Scripts

### CSS Files

- `static/Style.css`: Public-facing page styles.
- `static/admin.css`: Admin panel styles.
- `static/login.css`: Admin login page styles.

### JavaScript Files

- `static/js/graph.js`: Builds admin dashboard charts with Chart.js.
- `static/js/registerFilter.js`: Filters participant rows by game on the registered students page.
- `static/js/pdfdata.js`: Sends filtered rows to the backend and downloads the generated PDF.
- `static/js/studyAdmission.js`: Handles interactive sections on the studies and admission page.

### Images

- `static/images/college.jpg.avif`: College image asset used by the frontend.

## Common Workflows

### Add an Athletic Event Manually

1. Log in at `/admin-login`.
2. Open `/manage-athletic`.
3. Enter event name, date, time, and judges.
4. Submit the form.
5. Visit `/athletic` to confirm the event appears.

### Upload Athletic Events by CSV

1. Log in at `/admin-login`.
2. Open `/manage-athletic`.
3. Select a CSV file with the required header.
4. Click upload.
5. Visit `/athletic` to confirm the uploaded events.

### Add a Sports Event Manually

1. Log in at `/admin-login`.
2. Open `/manage-sports`.
3. Enter event name, date, time, and judges.
4. Submit the form.
5. Visit `/sports` to confirm the event appears.

### Upload Sports Events by CSV

1. Log in at `/admin-login`.
2. Open `/manage-sports`.
3. Select a CSV file with the required header.
4. Click upload.
5. Visit `/sports` to confirm the uploaded events.

### Register as a Student

1. Open `/athletic` or `/sports`.
2. Click `Register Yourself`.
3. Fill in student details.
4. Select one or more events.
5. Submit the form.

### Export Participants

1. Log in as admin.
2. Open `/manage-registered`.
3. Select an event from the dropdown.
4. Click `Download PDF`.

### Clear All Registrations

1. Log in as admin.
2. Open `/manage-registered`.
3. Click `Clear All`.
4. Confirm the browser prompt.

This deletes every row from the `GamesRegister` table.

## Troubleshooting

### The App Starts but Pages Show Empty Event Lists

The database may not contain athletic or sports events yet. Add events manually from the admin panel or upload `athletic.csv` and `sports.csv`.

### Admin Login Fails

Check that the `admin` table contains a user with the email and password you are entering. Passwords are currently stored in the `passwd` column.

### CSV Upload Does Not Add Events

Check the following:

- The file extension is `.csv`.
- The header is exactly `eventName,date,time,judges`.
- The date format is `YYYY-MM-DD`.
- The time format is `HH:MM`.
- Judge names containing commas are wrapped in quotes.

### Event Pages Crash When Displaying Dates or Times

The app parses event dates with:

```python
datetime.strptime(event.date, "%Y-%m-%d")
```

It parses event times with:

```python
datetime.strptime(event.time, "%H:%M")
```

If a row contains a different date or time format, the page can fail. Fix the affected database row or re-upload the CSV with the correct format.

### Dashboard Charts Do Not Load

The admin dashboard loads Chart.js from:

```text
https://cdn.jsdelivr.net/npm/chart.js
```

If there is no internet connection or the CDN is blocked, the charts may not render.

### Port 5000 Is Already in Use

Change the port in `main.py`:

```python
app.run(host="0.0.0.0", port=5001, debug=True)
```

Then run the project again and open:

```text
http://localhost:5001
```

## Security Notes

This project is currently set up like a student/development project, not a production-ready deployment.

Important limitations:

- The Flask secret key is hard-coded in `main.py`.
- Admin passwords are stored as plain text.
- Admin authentication checks email and password directly from the database.
- There is no CSRF protection on forms.
- Delete operations are available through GET/POST routes.
- Debug mode is enabled.
- Input validation is basic.
- The SQLite database file is stored locally in the project instance folder.

Before production use:

- Move secrets to environment variables.
- Hash passwords with Werkzeug or another password hashing library.
- Disable debug mode.
- Add CSRF protection.
- Add stronger form validation.
- Restrict destructive actions to POST requests.
- Add proper error handling for CSV import and date parsing.
- Add authorization checks for every admin-only action.
- Avoid committing real production database files.

## Future Improvements

- Add password hashing.
- Add a first-admin setup command.
- Add edit/update pages for events and notices.
- Add pagination for registrations and contacts.
- Add CSV validation with user-friendly error messages.
- Add search for participants.
- Add export for all participants.
- Add event category reporting.
- Add automated tests for routes and models.
- Move Chart.js to local static assets for offline use.
- Add environment-based configuration for development and production.
