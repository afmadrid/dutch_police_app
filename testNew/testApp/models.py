from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_cryptography.fields import encrypt


class Profile(models.Model):
    """Create Profile Table."""
    # Profile has a foreign key from User table with one to one relationship.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Personal Information will be encrypted before stored in the database.
    personal_information = encrypt(models.TextField(max_length=500, blank=True))
    address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # Users photo will be stored in profile_photos folder.
    photo = models.ImageField(default='default.png', upload_to='profile_photos')

    def __str__(self):
        return self.user.username


class Case(models.Model):
    """#Create Case Table."""
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=15,unique=True)
    description = models.TextField(max_length=200, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)
    # Here is the user who create or update the case as a foreign key from User table with many to one relation.
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    evidence = encrypt(models.ImageField(default='default.png', upload_to='case-evidence/', blank=True))

    def __str__(self):
        return self.title
