from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages


class CustomLoginView(LoginView):
    template_name = 'managementApps/registration/login.html'
    success_url = 'managementApps/home.html'


def root_page(request):
    return render(request, 'managementApps/registration/login.html')


@login_required
def home(request):
    
    return render(request, 'managementApps/home.html')

@login_required
def site(request):
    return render(request, 'managementApps/content/site.html')

@login_required
def partner(request):
    return render(request, 'managementApps/content/partner.html')
