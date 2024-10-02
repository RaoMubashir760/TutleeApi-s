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

class AdditionalInfo(models.Model):
    student = models.OneToOneField(TutleeUser, null = False, blank = True, related_name='student_against_this_info', on_delete = models.CASCADE)
    age = models.IntegerField(null = False, blank = False)
    location = models.CharField(max_length = 100, null = False, blank = False)
    picture = models.ImageField(upload_to = 'student_pictures/', null = True, blank = True)
    school_name = models.CharField(max_length = 255, null = True, blank = True)   
    short_term_goals = models.TextField(null = True, blank = True)
    long_term_goals = models.TextField(null = True, blank = True)

    def __str__(self):
        return f"Additional Info for {self.student}"
    
class Prefrences(models.Model):
    student = models.OneToOneField(TutleeUser, null=False, blank=False, related_name='student_against_these_preferences', on_delete=models.CASCADE)
    subjects_of_interest = models.TextField(null = True, blank = True)  
    learning_goals = models.TextField(null = True, blank = True) 
    preferred_learning_style = models.CharField(max_length = 255, null = True, blank = True) 
    study_schedule_preferences = models.TextField(null = True, blank = True) 
    mode_of_learning = models.CharField(max_length = 255, null = True, blank = True)  
    tutoring_preference = models.CharField(max_length = 255, null = True, blank = True)  
    frequency_of_tutoring = models.CharField(max_length = 255, null = True, blank = True) 

    def __str__(self):
        return f"Prefrences of {self.student}"
