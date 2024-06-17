from django.db import models
from django.http import HttpResponse
from datetime import date
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


def HomePage(request):
    return HttpResponse("<h1>Hello World</h1>")

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class JobListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    overview = models.TextField(default="")  # Provide a default value here
    requirements = models.TextField(default="")  # Provide a default value here
    responsibilities = models.TextField()
    skills_needed = models.TextField()
    image = models.CharField(max_length=100, blank=True)
    date_added = models.DateField(default=date.today)
    last_day_to_apply = models.DateField(default=date.today)
    experience_level = models.CharField(max_length=50, default='Mid')
    remote = models.CharField(max_length=50, default='Hybrid')
    job_type = models.CharField(max_length=50, default='Full-time')
    industry = models.CharField(max_length=100, default='Null')
    category = models.CharField(max_length=100, default='General')

    def __str__(self):
        return self.job_title
