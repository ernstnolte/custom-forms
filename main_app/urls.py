from django.urls import path
from . import views

urlpatterns = [
    # Form component view paths
    path('forms', views.getForms, name='getForms'),
    path('form/<int:form_id>', views.getFormDetail, name='getFormDetail'),
    path('form/<int:form_id>/responses', views.getFormResponses, name='getResponses'),
    path('response/<int:filled_form_id>', views.getResponseDetail, name='getResponseDetail'),

    # Form component creation paths
    path('form/create', views.createForm, name='createForm'),
    path('form/<int:form_id>/create/addGroup', views.createAddGroup, name='createAddGroup'),
    path('form/group/<int:group_id>/addFields', views.createAddFields, name='createAddFields'),
    path('form/field/<int:field_id>/addOptions', views.createAddOptions, name='createAddOptions'),
    path('form/<int:form_id>/send-response', views.createFilledForm, name='createFilledForm'),

    # Form component deletion paths
    path('form/<int:form_id>/delete', views.deleteForm, name='deleteForm'),
    path('group/<int:group_id>/delete', views.deleteGroup, name='deleteGroup'),
    path('field/<int:field_id>/delete', views.deleteField, name='deleteField'),
    path('option/<int:option_id>/delete', views.deleteOption, name='deleteOption'),
    path('response/<int:filled_form_id>/delete', views.deleteFilledForm, name='deleteFilledForm'),
]