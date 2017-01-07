from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^users/signin/$', views.signin_view, name='signin'),
    # url(r'^users/signout/$', views.signout_view, name='signout'),
    # url(r'^users/auth/$', views.auth_view, name='auth'),
    # url(r'^users/authorized/$', views.authorized_view, name='authorized'),
    # url(r'^users/baduser/$', views.baduser_view, name='baduser'),
    #
    # url(r'^users/signup/$', views.signup_view, name='signup'),
    # url(r'^users/signup_success/$', views.signup_success, name='signup_success'),

    url(r'^$', views.cabinet, name='cabinet'),
    url(r'^submit/$', views.submit_stego_object, name='submit_stego'),
    url(r'^extract/$', views.extract_stego_object, name='extract_stego'),
    # url(r'^feedback/$', views.feedback, name='feedback'),
    # url(r'^stego/uploaded/$', views.uploaded_object, name='uploaded_stego'),
    # url(r'^stego/extracted/$', views.extracted_object, name='extracted_stego'),
    # url(r'^stego/history/$', views.stego_history, name='stego_history'),
    # url(r'^clear/$', views.clear_stego_object, name='stego_clear'),
    # url(r'^stego/locale', views.view_locale, name='locale'),


]
