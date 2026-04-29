from django.core.mail import send_mail


def send_borrow_email(user, book, status):
    """
    Send email to user when borrow request is approved/rejected
    """

    subject = f"Book Borrow {status.capitalize()}"

    message = f"""
Hello {user.username},

Your request for the book "{book.title}" has been {status.lower()}.

Thank you,
Library Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email="admin@lms.com",
        recipient_list=[user.email],
        fail_silently=True,
    )