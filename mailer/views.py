import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import ComposeForm, RegisterForm
from .models import SentEmail


def register_view(request):
    if request.user.is_authenticated:
        return redirect('compose')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('compose')
    return render(request, 'mailer/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('compose')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('compose')
    return render(request, 'mailer/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def compose_view(request):
    form = ComposeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        to_addr = form.cleaned_data['to']
        cc_addr = form.cleaned_data.get('cc', '')
        subject = form.cleaned_data['subject']
        body = form.cleaned_data['body']
        attachment_file = request.FILES.get('attachment')

        # Build MIME message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = to_addr
        if cc_addr:
            msg['Cc'] = cc_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{attachment_file.name}"',
            )
            msg.attach(part)

        # Send via SMTP
        try:
            all_recipients = [a.strip() for a in to_addr.split(',')]
            if cc_addr:
                all_recipients += [a.strip() for a in cc_addr.split(',')]

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.ehlo()
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER, all_recipients, msg.as_string())

            # Save to DB
            sent = SentEmail(
                sender=request.user,
                to=to_addr,
                cc=cc_addr,
                subject=subject,
                body=body,
            )
            if attachment_file:
                attachment_file.seek(0)
                sent.attachment.save(attachment_file.name, attachment_file, save=False)
            sent.save()

            messages.success(request, 'Email sent successfully!')
            return redirect('sent')
        except smtplib.SMTPAuthenticationError:
            messages.error(request, 'SMTP authentication failed. Check your Gmail App Password in .env.')
        except smtplib.SMTPException as e:
            messages.error(request, f'Failed to send email: {e}')

    return render(request, 'mailer/compose.html', {'form': form})


@login_required
def sent_view(request):
    emails = SentEmail.objects.filter(sender=request.user)
    return render(request, 'mailer/sent.html', {'emails': emails})


@login_required
def email_detail_view(request, pk):
    try:
        email = SentEmail.objects.get(pk=pk, sender=request.user)
    except SentEmail.DoesNotExist:
        messages.error(request, 'Email not found.')
        return redirect('sent')
    return render(request, 'mailer/email_detail.html', {'email': email})
