from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from core.models import User
# Create your views here.


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
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
