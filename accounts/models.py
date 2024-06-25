from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Is Required")
        user = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length = 15, choices = GENDER, default = 'patient')
    email = models.EmailField(max_length=255, unique=True)
    age = models.IntegerField(blank=True, null=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'gender']


class ChronicDiseases(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_chronic_disease')
    diabetes = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)

class Allergy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_allergy')
    sea_food = models.BooleanField(default=False)
    lactose = models.BooleanField(default=False)
    egg = models.BooleanField(default=False)
    gluten = models.BooleanField(default=False)


@receiver(post_save, sender = CustomUser)
def createChronicDiseasesAndAllergy(sender, instance = None, created = False, *args, **kwargs):
    if created:
        ChronicDiseases.objects.create(
            user = instance
        )
        Allergy.objects.create(
            user = instance
        )