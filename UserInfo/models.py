from django.db import models
from django.contrib.auth.models import AbstractUser

class TutleeUser(AbstractUser):
    created_by = models.OneToOneField('self', null = True, on_delete = models.CASCADE)
    email = models.EmailField(null = False, blank = False, unique = True)
    username = models.EmailField(null = False, blank = False, unique = True)
    address = models.CharField(null = False, blank = False, default = 'Lahore', max_length = 100)
    first_name = models.CharField(blank = False, max_length = 50)
    last_name = models.CharField(blank = False, max_length = 50)
   
    def __str__(self):
        return f'{self.first_name}'
    class Meta:
        verbose_name = 'TutleeUser'

        


