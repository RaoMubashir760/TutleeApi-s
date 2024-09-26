from rest_framework import serializers
from UserInfo.models import TutleeUser
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
        instance.username = validated_data.get('email', instance.email)
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
        
class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required = True)
    password = serializers.CharField(write_only = True, required = True)










