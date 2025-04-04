import os
from email.mime.image import MIMEImage
from typing import List

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from voya.common.forms import SearchForm
from voya.common.tokens import account_activation_token

from voya.clients.models import ClientProfile
from voya.employees.models import EmployeeProfile


def get_user_obj(request):
    if request.user.is_authenticated and request.user.is_active:

        try:
            profile = ClientProfile.objects.get(user=request.user, is_active=True)

            return profile
        except ClientProfile.DoesNotExist:
            pass

        try:
            profile = EmployeeProfile.objects.get(user=request.user, is_active=True)

            return profile

        except EmployeeProfile.DoesNotExist:
            pass


def get_dashboard_multiple_search(request, queryset):
    """
        Performs a multiple field search on the given queryset based on user input.
    """

    search_form = SearchForm(request.GET)
    search_result = queryset

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        if search_query:
            model_fields = [
                field for field in queryset.model._meta.fields
                if field.name not in ['id', 'created_at'] and field.get_internal_type() not in ['OneToOneField']
            ]

            query = Q()

            # Build a Q object using the field__icontains lookup to search for the query.
            # Use the | operator to combine the Q objects into a single query.

            for field in model_fields:
                if isinstance(field, models.ForeignKey):
                    related_model = field.related_model
                    if hasattr(related_model, 'request') and hasattr(related_model.request, 'created_by_company'):
                        query |= Q(**{f'{field.name}__request__created_by_company__commercial_name__icontains': search_query})
                    if hasattr(related_model, 'request') and hasattr(related_model.request, 'slug'):
                        query |= Q(**{f'{field.name}__request__slug__icontains': search_query})
                    if hasattr(related_model, 'email'):
                        query |= Q(**{f'{field.name}__email__icontains': search_query})
                    if hasattr(related_model, 'slug'):
                        query |= Q(**{f'{field.name}__slug__icontains': search_query})
                else:
                    query |= Q(**{f'{field.name}__icontains': search_query})  # Searches in all text fields

            search_result = queryset.filter(query)

    return search_result


def generate_activation_token(request, user):
    # generate token
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # encodes user id

    # build activation URL
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )

    return activation_link


def send_activation_email(request, user):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo-voya.png')
    # generate token
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # encodes user id

    # build activation URL
    activation_link = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )

    # render HTML template
    html_content = render_to_string(
        template_name='emails/client-account-activation.html',
        context={
            'user': user,
            'activation_link': activation_link,
            'cid_logo': 'logo_image_cid',
        }
    )

    text_content = strip_tags(html_content)  # fallback text

    msg = EmailMultiAlternatives(
        subject='Activate your Voya account',
        body=text_content,
        from_email='voya@dromo.travel',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")

    # read the image file and attach it
    with open(image_path, 'rb') as f:
        msg_image = MIMEImage(f.read())
        msg_image.add_header('Content-ID', '<logo_image_cid>')
        msg_image.add_header('Content-Disposition', 'inline', filename='logo-voya.png')

    msg.attach(msg_image)

    # Add Content-ID header to be referenced via "cid:logo_image_cid"
    msg.mixed_subtype = 'related'
    last_attachment = msg.attachments[-1]
    last_attachment["Content-ID"] = "<logo_image_cid>"

    msg.send()


def send_custom_email(user, template_name, activation_link, email_subject, send_to: [], ):
    image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo-voya.png')

    # render HTML template
    html_content = render_to_string(
        template_name=template_name,
        context={
            'user': user,
            'activation_link': activation_link,
            'cid_logo': 'logo_image_cid',
        }
    )

    text_content = strip_tags(html_content)  # fallback text

    msg = EmailMultiAlternatives(
        subject=email_subject,
        body=text_content,
        from_email='voya@dromo.travel',
        to=send_to,
    )

    msg.attach_alternative(html_content, "text/html")

    # read the image file and attach it
    with open(image_path, 'rb') as f:
        msg_image = MIMEImage(f.read())
        msg_image.add_header('Content-ID', '<logo_image_cid>')
        msg_image.add_header('Content-Disposition', 'inline', filename='logo-voya.png')

    msg.attach(msg_image)

    # Add Content-ID header to be referenced via "cid:logo_image_cid"
    msg.mixed_subtype = 'related'
    last_attachment = msg.attachments[-1]
    last_attachment["Content-ID"] = "<logo_image_cid>"

    msg.send(fail_silently=False)
