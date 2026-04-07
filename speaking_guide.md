# Speaking Guide — Web-Based Email Application

---

## Timing Summary

| Slide | Speaker | Time |
|---|---|---|
| Title + Agenda | Gurkirat | 0:40 |
| Problem → Data model | Gurkirat | 4:30 |
| **Live demo** | Ratika | ~2:00 |
| Screenshots (10–13) | Ratika | 1:00 |
| Limitations | Either | 0:35 |
| Conclusion | Either | 0:45 |
| References | Either | 0:15 |

---

## Slide-by-Slide Script

### Slide 1 — Title (0:00–0:20)

> "Hi everyone. Today Ratika and I are presenting our Network Programming project — a web-based email application built with Django and Python's standard library. I'll cover the design and implementation in Part 1, and Part 2 will be the live demo with Ratika walking through the app."

---

### Slide 2 — Agenda (0:20–0:40)

> "Quick roadmap: Part 1 is the technical side — why we built this, what we used, and how the code actually works. Part 2 is the live demo followed by limitations and where we'd take it next."

---

### Slide 3 — Part 1 divider (0:40–0:45)

> "Let's start with why."

---

### Slide 4 — Problem statement (0:45–1:45)

> "We all use email every day — Gmail, Outlook — but it's a black box. The goal of this project was to rip that black box open. We wanted to understand what actually happens when you hit 'Send.'
>
> So the learning objectives were: understand the SMTP protocol, build MIME messages with attachments ourselves, handle user auth, and persist data in a database. No shortcuts — no `sendgrid`, no `yagmail` — just Python's stdlib."

---

### Slide 5 — Tech stack (1:45–2:30)

> "The stack is minimal by design. Python 3.14, Django 6 as the web framework. For email, we used only `smtplib` and `email.mime` from the standard library — that's the important constraint. The database is SQLite through Django's ORM, and the frontend is plain HTML and CSS.
>
> The key point here is that `smtplib` forces you to deal with the protocol directly — you're doing the TLS handshake, the auth, the MIME encoding yourself."

---

### Slide 6 — Application architecture (2:30–3:15)

> "The app follows Django's MVT pattern. Two packages: `emailapp` is the project config — settings, environment variables, root URLs. `mailer` is the core app — models, views, forms, and 6 URL routes.
>
> Request flow is: browser hits a route, Django calls the right view, the view runs the SMTP logic, saves to SQLite, and renders a template back. Straightforward, no async, no background workers."

---

### Slide 7 — SMTP email flow (code) (3:15–4:30)

> "This is the heart of the project. Let me walk through what happens when you send an email.
>
> First we build the MIME message — `MIMEMultipart` is the envelope. We set From, To, Subject headers, then attach the body as `MIMEText`.
>
> If there's a file attachment, we read the bytes, wrap them in `MIMEBase`, run `encode_base64` on it — that's the Base64 encoding you see in raw email headers — and attach it.
>
> Then we open a raw SMTP connection to Gmail on port 587. We call `ehlo` to identify ourselves, `starttls` to upgrade the connection to TLS — that's the encryption handshake — then `login` with credentials from the `.env` file, and finally `sendmail`. The `with` block closes the connection cleanly.
>
> This is exactly what Gmail's own client does under the hood — we're just doing it explicitly."

---

### Slide 8 — Data model (4:30–5:10)

> "Every email that goes out gets saved to SQLite. The `SentEmail` model has the obvious fields — sender, to, cc, subject, body, attachment path, and a timestamp. The `sender` is a foreign key to Django's built-in `auth_user` table, so each user only sees their own sent history.
>
> Passwords are stored as PBKDF2-SHA256 hashes — Django handles that automatically. Credentials for Gmail are in a `.env` file and excluded from git."

---

### Slide 9 — Part 2 divider (5:10–5:20)

> "That's the design side. Let's see it running. Ratika will walk through the demo."

---

## Live Demo (~5:20–7:20) — Ratika drives

Demo flow:
1. Open the app at `localhost:8000`
2. Show the register page — fill in username/email/password and submit
3. Show login — log in with those credentials
4. Go to Compose — fill To, CC, Subject, Body, attach a file
5. Hit Send — show the green success banner
6. Go to Sent folder — show the email in the list
7. Click the row — show the detail view and the download link

---

### Slide 10 — Register & login (7:20–7:40)

> "The auth is Django's built-in system. Registration validates password strength automatically. Passwords are hashed — users can't log in without a valid account, and only see their own sent emails."

---

### Slide 11 — Sending an email (7:40–8:00)

> "The compose form supports multiple recipients in To and CC, a text body, and an optional file. On success it shows a confirmation and redirects to Sent."

---

### Slide 12 — Sent folder (8:00–8:15)

> "The sent folder lists all emails for the current user, newest first. Clicking opens the full detail with a download link for attachments."

---

### Slide 13 — Example Email (8:15–8:25)

> "Here's an example of a received email — you can see the subject, body, and that the attachment came through correctly."

---

### Slide 14 — Limitations (8:25–9:00)

> "We're honest about what this doesn't do. It's send-only — no inbox, no IMAP. All mail goes out from one shared Gmail account, not from each user's own address. The SMTP settings are hardcoded for Gmail. No HTML email, no search, no pagination, and the dev server isn't production-ready.
>
> These aren't bugs — they're scope decisions. The focus was on understanding SMTP, not building a full mail client."

---

### Slide 15 — Conclusion & future improvements (9:00–9:45)

> "What we did achieve: a working email client built entirely on Python's stdlib, hands-on with the SMTP handshake, MIME structure, TLS, user auth, file attachments, and database persistence — all end to end.
>
> For future work — the most obvious next step is adding an inbox using `imaplib`. Per-user sending would need Gmail OAuth 2.0. For production you'd swap SQLite for Postgres and put Gunicorn and Nginx in front. Email scheduling could use Celery with Redis."

---

### Slide 16 — References (9:45–10:00)

> "The key references are the SMTP spec — RFC 5321 — and the MIME spec — RFC 2045. Plus the Python `smtplib` and `email.mime` docs and the Django 6 docs. Full list on the slide."

---

## Tips

- For the SMTP flow slide, point at each line as you speak — "this is the handshake, this is the TLS upgrade, this is where auth happens"
- Keep the demo tight — register + compose + send + view sent = 2 minutes max
- Don't read the limitations list — just hit the top 3 and move on
