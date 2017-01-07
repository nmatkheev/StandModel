from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Нужна generic-модель для всех методов. Видимо это нереал, ибо формы для методов будут заметно отличаться...
# class Method(models.Model):
#     method_name = models.CharField(max_length=50, unique=True)
#     # user_phrase = models.TextField()
#     # user_password = models.CharField(max_length=30)

class Document(models.Model):
    file = models.FileField(upload_to='files')


class Feedback(models.Model):
    email = models.EmailField(max_length=30)
    feedback = models.CharField(max_length=3000)

# class Document(models.Model):
#     upload_date = models.DateTimeField('date uploaded')
#     sender = models.ForeignKey(User)
#     sender_ip = models.IPAddressField
#     password = models.CharField(max_length=30, default='none')
#     payload = models.CharField(max_length=300, default='none')
#     method = models.ForeignKey(Method)
#     delivered = models.BooleanField()
#
#
# class SubmitFormModel(models.Model):
#     upload_date = models.DateTimeField()
#     sender = models.ForeignKey(User)
#     password = models.CharField(max_length=30, default='none')
#     payload = models.CharField(max_length=300, default='none')
#     method = models.ForeignKey(Method, to_field='method_name')
#     file = models.FileField(upload_to='files/%Y/%m/%d')
#     # method = models.ForeignKey(Method, to_field='method_name')



