from django.urls import path
from . import views

urlpatterns = [
    # Form component view paths
    path('forms', views.getForms, name='getForms'),
    path('forms/<int:form_id>', views.getFormDetail, name='getFormDetail'),
    path('forms/<int:form_id>/responses', views.getFormResponses, name='getResponses'),
    path('responses/<int:filled_form_id>', views.getResponseDetail, name='getResponseDetail'),

    # Form component creation paths
    path('forms/create', views.createForm, name='createForm'),
    path('forms/<int:form_id>/create/addGroup', views.createAddGroup, name='createAddGroup'),
    path('forms/group/<int:group_id>/addFields', views.createAddFields, name='createAddFields'),
    path('forms/field/<int:field_id>/addOptions', views.createAddOptions, name='createAddOptions'),
    path('forms/<int:form_id>/send-response', views.createFilledForm, name='createFilledForm'),

    # Form component deletion paths
    path('forms/<int:form_id>/delete', views.deleteForm, name='deleteForm'),
    path('forms/group/<int:group_id>/delete', views.deleteGroup, name='deleteGroup'),
    path('forms/field/<int:field_id>/delete', views.deleteField, name='deleteField'),
    path('forms/option/<int:option_id>/delete', views.deleteOptionFormField, name='deleteOptionFormField'),
    path('forms/responses/<int:filled_form_id>/delete', views.deleteFilledForm, name='deleteFilledForm'),

    # User authentication paths
    path("auth/csrf", views.csrf_token, name="csrf-token"),
    path("auth/user", views.current_user, name="current-user"),
    path("auth/signup", views.signup, name="signup"),
    path("auth/login", views.login_user, name="login"),
    path("auth/logout", views.logout_user, name="logout"),
]