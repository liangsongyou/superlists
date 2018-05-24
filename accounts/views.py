from django.core.mail import send_mail
from django.shortcuts import redirect,render
from django.contrib import messages, auth
from django.core.urlresolvers import reverse

from accounts.models import Token
from superlists.settings import EMAIL_HOST_USER

import sys

# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    print(email)
    send_mail(
        'Your login link for Superlists',
        message_body,
        EMAIL_HOST_USER,
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    # messages.add_message(
    #     request,
    #     messages.SUCCESS,
    #     "Check your email, we've sent you a link you can use to log in."
    # )
    return redirect('/')

def login(request):
    # print('login view', file=sys.stderr)
    # uid = request.GET.get('uid')
    user = auth.authenticate(uid=request.GET.get('token'))
    if user is not None:
        auth.login(request, user)
    return redirect('/')