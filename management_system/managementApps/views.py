from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Site, Partner
from django.views.decorators.csrf import csrf_exempt

class CustomLoginView(LoginView):
    template_name = 'managementApps/registration/login.html'
    success_url = 'managementApps/home.html'


def root_page(request):
    return render(request, 'managementApps/registration/login.html')

def signup(request):
    return render (request,'managementApps/registration/signup.html')


@login_required
def home(request):

    return render(request, 'managementApps/home.html')


@login_required
def site(request):
    alertMessage=""
    if request.method == 'POST':
        sitename = request.POST.get('sitename')
        sitekey = request.POST.get('sitekey')
        site = Site(sitename=sitename, sitekey=sitekey)

        if (sitename == "" or sitekey == ""):
          alertMessage="Site Name & Site Key Cannot be Empty!!"
        else:
           site.save()

    sites = Site.objects.all().order_by('site_id')
    return render(request, 'managementApps/content/site.html',{'sites':sites,'alert':alertMessage})


@login_required
def partner(request):
    alertMessage=""
    if request.method == 'POST':
        partnername = request.POST.get('partnername')
        partnerkey = request.POST.get('partnerkey')
        partner = Partner(partnername=partnername, partnerkey=partnerkey)

        if (partnername == "" or partnerkey == ""):
          alertMessage="Partner Name & Partner Key Cannot be Empty!!"
        else:
            partner.save()

       

    partners = Partner.objects.all().order_by('partner_id')
    return render(request, 'managementApps/content/partner.html',{'partners':partners,'alert':alertMessage})


def update_site(request, site_id):
    site = get_object_or_404(Site, site_id=site_id)

    if request.method == 'POST':
        # Retrieve the updated data from the request
        name = request.POST.get('sitename')
        sitekey = request.POST.get('sitekey')
        # Update the site object with the new data
        site.sitename = name
        site.sitekey = sitekey
        site.save()
        sites = Site.objects.all().order_by('site_id')
        return render(request, 'managementApps/content/site.html', {'site': site,'sites':sites})
    
    
    return render(request, 'managementApps/content/update_site.html', {'site': site})


def update_partner(request, partner_id):
    partner = get_object_or_404(Partner, partner_id=partner_id)

    if request.method == 'POST':
        # Retrieve the updated data from the request
        name = request.POST.get('partnername')
        partnerkey = request.POST.get('partnerkey')
        # Update the site object with the new data
        partner.partnername = name
        partner.partnerkey = partnerkey
        partner.save()
        partners = Partner.objects.all().order_by('partner_id')
        return render(request, 'managementApps/content/partner.html', {'partner': partner,'partners':partners})
    
    
    return render(request, 'managementApps/content/update_partner.html', {'partner': partner})