# Gestion des mails 

## Les configurations (importations)

from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import os
from email.mime.image import MIMEImage

## La fonction pour générer un email avec template 

def send_mail(request,template, to, title, subject, user, password, role, annee):
    html_content = render_to_string(template,{"title":title,"user": user,"password":password,"role": role, "annee": annee}) 
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        #subject
        subject,
        #content
        text_content,
        #from 
        EMAIL_HOST_USER,
        #to
         [to]

    )
    email.attach_alternative(html_content, "text/html")
    img_dir = 'static/img'
    # Image En-tete
    image = 'logo.png'
    file_path = os.path.join(img_dir, image)
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)

    # Image Pied 
    image2 = 'ept.png'
    file2_path = os.path.join(img_dir, image2)
    with open(file2_path, 'rb') as f:
        img2 = MIMEImage(f.read())
        img2.add_header('Content-ID', '<{name}>'.format(name=image2))
        img2.add_header('Content-Disposition', 'inline', filename=image2)
    
    
    email.attach(img)
    email.attach(img2)

    email.send()