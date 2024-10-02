from rest_framework import serializers
from UserInfo.models import TutleeUser, AdditionalInfo, Prefrences
from django.core.mail import send_mail
from django.conf import settings

class TutleeUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)
    class Meta:
        model = TutleeUser
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'password', 'confirm_password']

    def create(self, validated_data):
        useremail = validated_data['email']
        password = validated_data['password']
        address = validated_data['address']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user=TutleeUser.objects.create(username = useremail, email = useremail, first_name = first_name, last_name = last_name, address = address)
        user.set_password(password)
        user.save()
        user.created_by = user 
        user.save()
        email_sending_function(first_name, useremail)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('email', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
             
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Your confirming password is not matching!!')
        else:
             return data
    
def email_sending_function(username, useremail):
    subject = 'Welcome to Tutlee'
    message = f'Hi {username},\n\nThank you for registering with us. We are excited to have you on board!'
    email_from = settings.DEFAULT_FROM_EMAIL  # Set the sender's email
    recipient_list = [useremail]  # Send email to the registered user's email
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)

class AdditionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['age', 'location', 'picture', 'school_name', 'short_term_goals', 'long_term_goals']

    def create(self, validated_data):
        student = self.context['student']
        try:
            user_info = AdditionalInfo.objects.get(student = student)
            # If the record exists, you can either update or return an error
            raise serializers.ValidationError(f"AdditionalInfo for this student already exists.{user_info}")
        except AdditionalInfo.DoesNotExist:
            age = validated_data['age']
            location = validated_data['location']
            picture = validated_data['picture']
            school_name = validated_data['school_name']
            short_term_goals = validated_data['short_term_goals']
            long_term_goals = validated_data['long_term_goals']
            user = AdditionalInfo.objects.create(
                                    student = student,
                                    age = age,
                                    picture = picture,
                                    location = location,
                                    school_name = school_name,
                                    short_term_goals = short_term_goals,
                                    long_term_goals = long_term_goals 
                                )
            user.save()
            return user

    def update(self, instance, validated_data):
            instance.age = validated_data.get('age', instance.age)
            instance.location = validated_data.get('location', instance.location)
            instance.school_name = validated_data.get('school_name', instance.school_name)
            instance.short_term_goals = validated_data.get('short_term_goals', instance.short_term_goals)
            instance.long_term_goals = validated_data.get('long_term_goals', instance.long_term_goals)
            instance.picture = validated_data.get('picture', instance.picture)
            instance.save()
            return instance

class PrefrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prefrences
        fields = ['subjects_of_interest', 'learning_goals', 'tutoring_preference', 'frequency_of_tutoring_sessions',
                  'preferred_learning_style', 'study_schedule_preferences', 'mode_of_learning']

    def create(self, validated_data):
        student = self.context['student']
        try:
            user_info = Prefrences.objects.get(student = student)
            # If the record exists, you can either update or return an error
            raise serializers.ValidationError(f"AdditionalInfo for this student already exists.{user_info}")
        except Prefrences.DoesNotExist:
            subjects_of_interest = validated_data['subjects_of_interest']
            learning_goals = validated_data['learning_goals']
            tutoring_preference = validated_data['tutoring_preference']
            frequency_of_tutoring_sessions = validated_data['frequency_of_tutoring_sessions']
            preferred_learning_style = validated_data['preferred_learning_style']
            study_schedule_preferences = validated_data['study_schedule_preferences']
            mode_of_learning = validated_data['mode_of_learning']
            user = Prefrences.objects.create(
                                    student = student,
                                    subjects_of_interest = subjects_of_interest,
                                    learning_goals = learning_goals,
                                    tutoring_preference = tutoring_preference,
                                    frequency_of_tutoring_sessions = frequency_of_tutoring_sessions,
                                    preferred_learning_style = preferred_learning_style,
                                    study_schedule_preferences = study_schedule_preferences,
                                    mode_of_learning = mode_of_learning
                                )
            user.save()
            return user

    def update(self, instance, validated_data):
            instance.subjects_of_interest = validated_data.get('subjects_of_interest', instance.subjects_of_interest)
            instance.subjects_of_interest = validated_data.get('subjects_of_interest', instance.subjects_of_interest)
            instance.learning_goals = validated_data.get('learning_goals', instance.learning_goals)
            instance.tutoring_preference = validated_data.get('tutoring_preference', instance.tutoring_preference)
            instance.frequency_of_tutoring_sessions = validated_data.get('frequency_of_tutoring_sessions', instance.frequency_of_tutoring_sessions)
            instance.preferred_learning_style = validated_data.get('preferred_learning_style', instance.preferred_learning_style)
            instance.study_schedule_preferences = validated_data.get('study_schedule_preferences', instance.study_schedule_preferences)
            instance.mode_of_learning = validated_data.get('mode_of_learning', instance.mode_of_learning)
            instance.save()
            return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required = True)
    password = serializers.CharField(write_only = True, required = True)










