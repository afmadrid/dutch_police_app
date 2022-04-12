from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')

    def __str__(self):
        return self.user.username

        #resize the image and save
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class Case(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=15,unique=True)
    description = models.TextField(max_length=200, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    FIR = models.ImageField(default='default.png', upload_to='case_FIR', blank=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    firstName = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank = True, null = True)
    #address = models.TextField(blank=True, null=True)
    #description = models.TextField(blank=True, null=True)
    #createdAt = models.DateTimeField("Created At", auto_now_add=True)
def __str__(self):
    return self.firstName
