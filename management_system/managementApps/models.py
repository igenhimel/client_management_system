from django.db import models

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    sitename = models.CharField(max_length=100)
    sitekey = models.CharField(max_length=100)
    dns = models.CharField(max_length=16)
    company_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)


class Partner(models.Model):
    partner_id = models.AutoField(primary_key=True)
    partnername = models.CharField(max_length=100)
    partnerkey = models.CharField(max_length=100)
    dns = models.CharField(max_length=16)
    company_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)


    
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)  # You should consider using a more secure way to store passwords.
    
    SUPERUSER_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    superuser = models.CharField(max_length=3, choices=SUPERUSER_CHOICES, default='no')
    
    READ_PERMISSION = 'read'
    WRITE_PERMISSION = 'write'
    
    PERMISSION_CHOICES = [
        (READ_PERMISSION, 'Read'),
        (WRITE_PERMISSION, 'Write'),
    ]
    permissions = models.CharField(max_length=255, choices=PERMISSION_CHOICES, default=READ_PERMISSION)

    def __str__(self):
        return self.username