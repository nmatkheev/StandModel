from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import formset_factory

# import magic //apt-get intsall python3-magic

from . import validators


# class MyRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
#
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Выбрать файл PDF / Select a PDF file', help_text='max. 13 megabytes', widget=forms.FileInput)

    def clean(self):
        from django.template.defaultfilters import filesizeformat
        from django.utils.translation import ugettext_lazy as _
        from django.conf import settings

        try:
            content = self.cleaned_data['docfile']
        except KeyError:
            raise forms.ValidationError(_('Загрузите PDF-файл!'))

        if content.content_type in settings.CONTENT_TYPES:
            if content.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Файл больше %s!') % \
                                            (filesizeformat(settings.MAX_UPLOAD_SIZE)))
        else:
            raise forms.ValidationError(_('Формат файла должен быть PDF!'))
        return content


class AttributesForm(forms.Form):
    password = forms.CharField(label='Пароль / Password', max_length=50, min_length=1)
    payload = forms.CharField(label='Сообщение / Message', max_length=3000, min_length=1, widget=forms.Textarea)

    # def __init__(self, *args, **kwargs):
    #     super(AttributesForm, self).__init__(*args, **kwargs)
    # Можно вставлять в форму что-то(радиокнопки к примеру -- стр 159 гринфилд)

    def clean(self):
        cleaned_data = super(AttributesForm, self).clean()
        password = cleaned_data.get("password", "")
        payload = cleaned_data.get("payload", "")

        psw = password.encode()
        if len(psw) > 56 or len(psw) < 5:
            msg = "Ключ должен быть не меньше 5 символов и не больше 56"
            raise forms.ValidationError(msg)
        if '^' in payload:
            msg = "Разрешены алфавитно-цифровые символы и знаки препинания!"
            raise forms.ValidationError(msg)
        # if not(validators.validate_cyrillic(password) and validators.validate_cyrillic(payload)):
        #     msg = "Разрешены только латинские буквы и знаки препинания"
        #     raise forms.ValidationError(msg)
        return cleaned_data


class ExtractForm(forms.Form):
    password = forms.CharField(label='Пароль / Password', max_length=50, min_length=1)

    def clean(self):
        cleaned_data = super(ExtractForm, self).clean()
        password = cleaned_data.get("password", "")

        psw = password.encode()
        if len(psw) > 56 or len(psw) < 5:
            msg = "Ключ должен быть не меньше 5 символов и не больше 56"
            raise forms.ValidationError(msg)
        # if not validators.validate_cyrillic(password):
        #     msg = "Разрешены только латинские буквы и знаки препинания"
        #     raise forms.ValidationError(msg)
        return cleaned_data

    # class SubmitStegoObject(ModelForm):
    #
    #     class Meta:
    #         model = SubmitFormModel
    #         fields = ('method', 'password', 'payload')

    # def save(self, commit=True):
    #     import time, datetime
    #     ts = time.time()
    #     st = datetime.datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
    #
    #     self.Meta.model.upload_date = st


# class FeedbackForm(forms.Form):
#     email = forms.EmailField(label='Ваш email / Your email', max_length=30, min_length=7, widget=forms.EmailInput)
#     message = forms.CharField(label='Ваше сообщение / Your message', max_length=3000, min_length=10, widget=forms.Textarea)

    # def clean(self):
    #     cleaned_data = super(FeedbackForm, self).clean()
    #     email = cleaned_data.get("password", "")
    #
    #
    #     # if not validators.validate_cyrillic(password):
    #     #     msg = "Разрешены только латинские буквы и знаки препинания"
    #     #     raise forms.ValidationError(msg)
    #     return cleaned_data