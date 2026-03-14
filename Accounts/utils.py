import threading
from django.core.mail import send_mail
from django.conf import settings


def send_email_threading(subject, message, recipient_email):
    def send():
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

    thread = threading.Thread(target=send)
    thread.start()