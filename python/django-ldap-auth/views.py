from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template import RequestContext


def login_user(request):

    username = password = ""
    state = ""

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        print username, password

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            state = "Valid account"
        else:
            state = "Inactive account"
    return render_to_response('auth_user/auth.html', RequestContext(request, {'state': state, 'username': username}))
