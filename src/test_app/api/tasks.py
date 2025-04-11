from celery import shared_task
import random
from api.models import Node
from django.db.models import Q, F
import qrcode
from django.core.mail import EmailMessage
from io import BytesIO


@shared_task
def increase_debt():
    debt_increase = random.randint(5, 500)
    queryset = Node.objects.filter(~Q(name="Завод"))
    queryset.update(debt=F("debt") + debt_increase)
    print(f"Задолженность увеличена на {debt_increase}.")


@shared_task
def decrease_debt():
    debt_decrease = random.randint(100, 10000)
    queryset = Node.objects.filter(~Q(name="Завод"))
    queryset.update(debt=F("debt") - debt_decrease)
    print(f"Задолженность уменьшена на {debt_decrease}.")


@shared_task
def clear_debt_task(ids: list):
    Node.objects.filter(id__in=ids).update(debt=0)


@shared_task
def send_mail_with_qr(email, contact_data):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(contact_data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    subject = "Ваш QR код"
    message = "Пожалуйста, найдите ваш QR код в приложении."
    email = EmailMessage(subject, message, to=[email])
    email.attach("qr_code.png", buffer.read(), "image/png")
    email.send()
