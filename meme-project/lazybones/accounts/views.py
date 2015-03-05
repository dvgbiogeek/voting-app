from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from accounts.forms import UserCreateForm


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/login')
    else:
        form = UserCreateForm()
    return render(request, 'new_account.html', {'form': form})
