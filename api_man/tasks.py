from celery import Celery
from celery import shared_task
from django.template import Context, Template
from django.utils.timezone import now
from django.contrib.sites.models import Site
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from api_man.models import *

from urllib.request import urlopen
from django.core.files import File
from tempfile import NamedTemporaryFile
import os


def send_email(subject, to_mail, html, plain_text=None, cc_mails=None):
    # Gmail SMTP Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "rishukumargupta.offical@gmail.com"         # Replace with your Gmail address
    SMTP_PASSWORD = "lchdbgwtsregomin"            # Use App Password if 2FA is enabled
    SMTP_TLS = True

    # Email Details
    sender_email = SMTP_USERNAME
    recipients = to_mail if isinstance(to_mail, list) else [to_mail]
    
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    # Optional CC
    if cc_mails:
        cc_recipients = cc_mails if isinstance(cc_mails, list) else [cc_mails]
        msg["Cc"] = ", ".join(cc_recipients)
        recipients += cc_recipients

    # Attach plain text and HTML content
    if plain_text:
        msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_TLS:
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def file_from_url(image_url):
    try:
        img_temp = NamedTemporaryFile(delete=True)
        with urlopen(image_url) as u:
            img_temp.write(u.read())
        img_temp.flush()

        filename = os.path.basename(image_url.split('?')[0]) or "image_from_url"

        return File(img_temp, name=filename)

    except Exception as e:
        print(f"Error downloading file from {image_url}: {e}")
        return None


@shared_task
def push_rapiad_movie_data(response):
    for key,data in response.items():
        
        countryCode=data.get('countryCode')
        countryName=data.get('name')
        
        print("country name:- ",countryName)

        country,created=Country.objects.get_or_create(
            country_code=countryCode,
            defaults={
                "name":countryName
            }
        )

        for service in data.get('services',[]):
            service_slug=service.get('id')
            service_name=service.get('name')
            service_home_page_url=service.get('homePage')
            service_platform_themeColorCode=service.get('themeColorCode')
            service_platform_streamingOptionTypes=service.get('streamingOptionTypes')
            
            service_platform_imageSet=service.get('imageSet')
            
            plat_form,created=AvaiablePlatformServiceByCountry.objects.get_or_create(
                slug=service_slug,
                country=country,
                defaults={
                    "name":service_name,
                    "platform_home_url":service_home_page_url,
                    "platform_themeColorCode":service_platform_themeColorCode,
                    "streamingOptionTypes":service_platform_streamingOptionTypes,
                }
            )
            lightThemeImage=None
            if service_platform_imageSet.get('lightThemeImage'):
                lightThemeImage=file_from_url(service_platform_imageSet.get('lightThemeImage'))
            
            
            darkThemeImage=None
            if service_platform_imageSet.get('darkThemeImage'):
                darkThemeImage=file_from_url(service_platform_imageSet.get('darkThemeImage'))
            
            whiteImage=None
            if service_platform_imageSet.get('whiteImage'):
                whiteImage=file_from_url(service_platform_imageSet.get('whiteImage'))
            
            print("lightThemeImage:- ",service_platform_imageSet.get('lightThemeImage'))
            print("darkThemeImage:- ",service_platform_imageSet.get('darkThemeImage'))
            print("whiteImage:- ",service_platform_imageSet.get('whiteImage'))
            
            platform_img=PlatformImage.objects.create(
                platform=plat_form,
                lightThemeImage=lightThemeImage,
                darkThemeImage=darkThemeImage,
                whiteImage=whiteImage,
            )
                    

    print("successfully inserted data!!!")




