from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Site, Partner, User
from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse
import jwt
import datetime
from django.contrib.auth.hashers import check_password
from .decorators import token_required
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.conf import settings
from decouple import config

SECRET_KEY = 'your-secret-key'


def root_page(request):
    return render(request, 'managementApps/auth/login.html')


@token_required
def home(request):
    return render(request, 'managementApps/home.html')


@token_required
def add_site(request):
    return render(request, 'managementApps/content/add_site.html')


@token_required
def site(request):
    alertMessage = ""
    username = request.session.get('username', '')
    current_user = User.objects.filter(
        username=request.session.get('username')).first()
    if request.method == 'POST':
        sitename = request.POST.get('sitename')
        sitekey = request.POST.get('sitekey')
        dns = request.POST.get('dns')
        company_name = request.POST.get('company_name')
        country_name = request.POST.get('country_name')
        site = Site(sitename=sitename, sitekey=sitekey, dns=dns,
                    company_name=company_name, country_name=country_name)

        if (sitename == "" or sitekey == "" or dns == "" or company_name == "" or country_name == ""):
            alertMessage = "Input Field Cannot be Empty!!"
        else:
            site.save()

    sites = Site.objects.all().order_by('site_id')
    return render(request, 'managementApps/content/site.html', {'sites': sites, 'alert': alertMessage, 'username': username, 'user': current_user})


@token_required
def update_site(request, site_id):
    site = get_object_or_404(Site, site_id=site_id)

    if request.session.get('username'):
        current_user = User.objects.filter(
            username=request.session.get('username')).first()
        if current_user and 'write' in current_user.permissions:
            if request.method == 'POST':
                # Retrieve the updated data from the request
                name = request.POST.get('sitename')
                sitekey = request.POST.get('sitekey')
                dns = request.POST.get('dns')
                company_name = request.POST.get('sitecompany')
                country_name = request.POST.get('sitecountry')
                # Update the site object with the new data
                site.sitename = name
                site.sitekey = sitekey
                site.dns = dns
                site.company_name = company_name
                site.country_name = country_name
                site.save()
                sites = Site.objects.all().order_by('site_id')
                return render(request, 'managementApps/content/site.html', {'site': site, 'sites': sites, 'user': current_user})

            return render(request, 'managementApps/content/update_site.html', {'site': site})
        else:
            return render(request, 'managementApps/error/401.html',  {'error': 'You are not allowed to update site'})


@token_required
def partner(request):
    alertMessage = ""
    current_user = User.objects.filter(
        username=request.session.get('username')).first()
    if request.method == 'POST':
        partnername = request.POST.get('partnername')
        partnerkey = request.POST.get('partnerkey')
        dns = request.POST.get('dns')
        company_name = request.POST.get('company_name')
        country_name = request.POST.get('country_name')
        partner = Partner(partnername=partnername, partnerkey=partnerkey,
                          dns=dns, company_name=company_name, country_name=country_name)

        if (partnername == "" or partnerkey == "" or dns == "" or company_name == "" or country_name == ""):
            alertMessage = "Input Field Cannot be Empty!!"
        else:
            partner.save()

    partners = Partner.objects.all().order_by('partner_id')
    return render(request, 'managementApps/content/partner.html', {'partners': partners, 'alert': alertMessage, 'user': current_user})


@token_required
def add_partner(request):
    return render(request, 'managementApps/content/add_partner.html')


@token_required
def update_partner(request, partner_id):
    partner = get_object_or_404(Partner, partner_id=partner_id)
    if request.session.get('username'):
        current_user = User.objects.filter(
            username=request.session.get('username')).first()
        if current_user and 'write' in current_user.permissions:
            if request.method == 'POST':
                # Retrieve the updated data from the request
                name = request.POST.get('partnername')
                partnerkey = request.POST.get('partnerkey')
                dns = request.POST.get('dns')
                company_name = request.POST.get('partnercompany')
                country_name = request.POST.get('partnercountry')
                # Update the site object with the new data
                partner.partnername = name
                partner.partnerkey = partnerkey
                partner.dns = dns
                partner.company_name = company_name
                partner.country_name = country_name
                partner.save()
                partners = Partner.objects.all().order_by('partner_id')
                return render(request, 'managementApps/content/partner.html', {'partner': site, 'partners': partners, 'user': current_user})

            return render(request, 'managementApps/content/update_partner.html', {'partner': partner, 'user': current_user})
        else:
            return render(request, 'managementApps/error/401.html',  {'error': 'You are not allowed to update partner'})


@token_required
def add_user(request):
    if request.method == 'POST':
        # Check if the user making the request is a superuser
        if request.session.get('username'):
            current_user = User.objects.filter(
                username=request.session.get('username')).first()
            if current_user and current_user.superuser == 'yes':
                # Retrieve form data
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                superuser = request.POST.get('superuser')
                permissions = request.POST.getlist('permissions')

                if permissions == []:
                    permissions = ['read']

                # Check if the username already exists
                existing_user = User.objects.filter(username=username).first()
                if existing_user:
                    return render(request, 'managementApps/auth/add_user.html', {'error': 'Username already exists'})

                # Create and save the user
                user = User(username=username, email=email, password=make_password(password),
                            superuser=superuser, permissions=','.join(permissions))
                user.save()

                users = User.objects.all().order_by('id')
                # Redirect to a page showing the user list or any other appropriate view
                return render(request, 'managementApps/auth/user_list.html', {'users': users})

        # If the user is not a superuser or not logged in, handle accordingly
        return render(request, 'managementApps/error/401.html', {'error': 'You are not allowed to create a user'})
    else:
        if request.session.get('username'):
            current_user = User.objects.filter(
                username=request.session.get('username')).first()
            if current_user and current_user.superuser == 'yes':
                return render(request, 'managementApps/auth/add_user.html')
            else:
                return render(request, 'managementApps/error/401.html',  {'error': 'You are not allowed to create a user'})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.filter(username=username).first()
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        if user and check_password(password, user.password):
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            # Decode the token to remove the 'b' prefix
            token = token.decode('utf-8')

            response = redirect('/app/home')
            # Set JWT as an HTTP-only cookie
            response.set_cookie('jwt', token, httponly=True)
            request.session['username'] = username

            return response
        else:
            return render(request, 'managementApps/auth/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'managementApps/auth/login.html')


@token_required
def logout_view(request):
    # Clear the JWT cookie by setting it to an empty string and expiring it immediately
    # Redirect to the login page after logout
    response = redirect('/app/login')
    response.set_cookie('jwt', '', expires=0)
    del request.session['username']
    return response


@token_required
def user_list(request):
    users = User.objects.all().order_by('id')
    if request.session.get('username'):
        current_user = User.objects.filter(
            username=request.session.get('username')).first()
        if current_user and current_user.superuser == 'yes':
            return render(request, 'managementApps/auth/user_list.html', {'users': users, })
        else:
            return render(request, 'managementApps/error/401.html',  {'error': 'You are not allowed to show this content'})


def update_user(request,id):
    user = get_object_or_404(User, id=id)
    if request.session.get('username'):
        current_user = User.objects.filter(username=request.session.get('username')).first()
        if current_user and 'write' in current_user.permissions:
            if request.method == 'POST':
                # Retrieve the updated data from the request
                username = request.POST.get('username')
                email = request.POST.get('email')
                superuser = request.POST.get('superuser')
                permissions = request.POST.getlist('permissions')

                # Update the site object with the new data
                user.username = username
                user.email = email
                user.superuser = superuser
                user.permissions = permissions
                user.save()
                users = User.objects.all().order_by('id')
                return render(request, 'managementApps/auth/user_list.html', {'users': users})

            return render(request, 'managementApps/auth/update_user.html', {'users': user})
        else:
            return render(request, 'managementApps/error/401.html',  {'error': 'You are not allowed to update User'})


def handler404(request, exception):
    return render(request, 'managementApps/error/404.html', locals())
