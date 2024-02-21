from django.core.mail import send_mail
import random
import string


token = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

send_mail(
    'Verification Code',
    f'Your verification code is: {token}',
    'sender@example.com',
    ['receiver@example.com'],  # Replace with the user's email
    fail_silently=False,
)
