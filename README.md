# WebMail — Web-Based Email Application

A college project demonstrating real-world email communication using Django and Python's `smtplib`. Users can register, log in, compose and send emails (with CC and attachments), and view their sent history — all through a browser-based interface.

---

## Features

- **User Authentication** — Register, login, and logout. Only authenticated users can send emails.
- **Compose Email** — Fill in To, CC (multiple addresses), Subject, Body, and an optional file attachment.
- **SMTP Sending** — Emails are sent through Gmail's SMTP server using Python's built-in `smtplib` and `email.mime` libraries.
- **Sent Folder** — Every sent email is saved to the database and viewable per user.
- **Email Detail View** — Click any sent email to see full details including the attachment download link.
- **File Attachments** — Supports PDFs, images, and other common file types.
- **Validation & Error Handling** — Form validation and SMTP error messages shown in the UI.

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Language   | Python 3                            |
| Framework  | Django 6                            |
| Database   | SQLite (Django default)             |
| Email      | `smtplib`, `email.mime` (stdlib)    |
| Protocol   | SMTP over TLS (port 587)            |
| Frontend   | HTML5, CSS3 (no JS frameworks)      |
| Auth       | Django's built-in auth system       |
| Config     | `python-dotenv` for credentials     |

---

## Project Structure

```
project/
├── emailapp/               # Django project config
│   ├── settings.py         # App settings, SMTP config
│   └── urls.py             # Root URL routing
├── mailer/                 # Core email app
│   ├── models.py           # SentEmail model
│   ├── views.py            # Login, register, compose, sent, detail
│   ├── forms.py            # ComposeForm, RegisterForm
│   └── urls.py             # App URL patterns
├── templates/
│   ├── base.html           # Shared layout with navbar
│   └── mailer/             # Page templates
│       ├── login.html
│       ├── register.html
│       ├── compose.html
│       ├── sent.html
│       └── email_detail.html
├── static/css/style.css    # App stylesheet
├── media/                  # Uploaded attachments (auto-created)
├── .env                    # Gmail credentials (not committed)
├── .gitignore
└── manage.py
```

---

## Setup & Running

### 1. Clone and create the virtual environment

```bash
git clone <repo-url>
cd project
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django python-dotenv
```

### 2. Configure Gmail credentials

Create a `.env` file in the project root:

```
EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

> **Gmail App Password required.** Your regular Gmail password won't work.
> To generate one: Google Account → Security → 2-Step Verification → App Passwords.

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Run the server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## How It Works

1. The user registers and logs in via Django's auth system.
2. On the Compose page, the form is submitted with `multipart/form-data` to support file uploads.
3. Django's view builds a `MIMEMultipart` message, attaches the body as `MIMEText`, and encodes any uploaded file as a `MIMEBase` attachment.
4. A raw SMTP connection is opened to `smtp.gmail.com:587`, upgraded to TLS via `STARTTLS`, and the message is sent using the credentials from `.env`.
5. On success, the email details are saved to the `SentEmail` table in SQLite and the user is redirected to the Sent folder.

---

## Team Contributions

### Gurkirat Singh
- Django project setup and configuration (`emailapp/settings.py`, virtual environment, `python-dotenv`)
- SMTP integration — raw `smtplib` connection, `STARTTLS`, authentication, and message dispatch
- MIME message construction — `MIMEMultipart`, `MIMEText`, `MIMEBase`, Base64 file encoding
- Data model design — `SentEmail` model, migrations, SQLite persistence
- URL routing and view structure

### Ratika
- User authentication — register, login, logout views using `django.contrib.auth`
- Compose form — `ComposeForm`, multi-recipient handling, file upload logic
- Sent folder and email detail views
- Frontend — HTML templates (`base.html`, all page templates), CSS stylesheet (`style.css`)
- Form validation and SMTP error handling in the UI

---

## Pages

| URL            | Page              | Auth required |
|----------------|-------------------|---------------|
| `/login/`      | Login             | No            |
| `/register/`   | Register          | No            |
| `/compose/`    | Compose Email     | Yes           |
| `/sent/`       | Sent Folder       | Yes           |
| `/sent/<id>/`  | Email Detail      | Yes           |
| `/logout/`     | Logout            | Yes           |
