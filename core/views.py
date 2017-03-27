from django.urls import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login
# Create your views here.


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:registration_complete'))

    else:
        form = MyUserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render_to_response('core/registration.html', token)


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('blogpost:mainpage'))
    else:
        return login(request, **kwargs)
