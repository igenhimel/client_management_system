from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Site, Partner, User
from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse



class CustomLoginView(LoginView):
    template_name = 'managementApps/auth/login.html'
    success_url = 'managementApps/home.html'


def root_page(request):
    return render(request, 'managementApps/auth/login.html')


def signup(request):
    return render(request, 'managementApps/registration/signup.html')


def home(request):

    return render(request, 'managementApps/home.html')


def add_site(request):
    return render(request, 'managementApps/content/add_site.html')


def site(request):
    alertMessage = ""
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
    return render(request, 'managementApps/content/site.html', {'sites': sites, 'alert': alertMessage})


def update_site(request, site_id):
    site = get_object_or_404(Site, site_id=site_id)

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
        return render(request, 'managementApps/content/site.html', {'site': site, 'sites': sites})

    return render(request, 'managementApps/content/update_site.html', {'site': site})


def partner(request):
    alertMessage = ""
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
    return render(request, 'managementApps/content/partner.html', {'partners': partners, 'alert': alertMessage})


def add_partner(request):
    return render(request, 'managementApps/content/add_partner.html')


def update_partner(request, partner_id):
    partner = get_object_or_404(Partner, partner_id=partner_id)

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
        return render(request, 'managementApps/content/partner.html', {'partner': site, 'partners': partners})

    return render(request, 'managementApps/content/update_partner.html', {'partner': partner})


def add_user(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        superuser = request.POST.get('superuser')
        permissions = request.POST.getlist('permissions')

        # Create and save the user
        user = User(username=username, email=email, password=password,
                    superuser=superuser, permissions=','.join(permissions))
        user.save()

        sites = Site.objects.all().order_by('site_id')
        # Redirect to a page showing user list or any other appropriate view
        return render(request, 'managementApps/content/site.html', {'sites': sites})
    else:
        return render(request, 'managementApps/auth/add_user.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Find the user by username in your custom User model
            user = User.objects.get(username=username)

            # Check the password
            if user.password == password:
                # Generate JWT token
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                print(token)
                return JsonResponse({'token': token})
        except User.DoesNotExist:
            pass

        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return render(request, 'managementApps/auth/login.html')



