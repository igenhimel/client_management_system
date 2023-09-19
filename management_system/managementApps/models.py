from django.db import models

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    sitename = models.CharField(max_length=100)
    sitekey = models.CharField(max_length=100)


class Partner(models.Model):
    partner_id = models.AutoField(primary_key=True)
    partnername = models.CharField(max_length=100)
    partnerkey = models.CharField(max_length=100)
