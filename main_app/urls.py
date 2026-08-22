from django.urls import path
from . import views

urlpatterns = [
    # Form view paths
    path('forms', views.getForms, name='getForms'),
    path('form/<int:pk>', views.getFormDetail, name='getFormDetail'),
    path('form/<int:pk>/responses', views.getFormResponses, name='getResponses'),
    path('response/<int:pk>', views.getResponseDetail, name='getResponseDetail'),

    # Form manip paths
    path('form/<int:form_id>/send-response', views.sendResponse, name='sendResponse'),
    path('form/create', views.createForm, name='createForm'),
    path('form/<int:form_id>/create/addGroup', views.createAddGroup, name='createAddGroup'),
    path('form/group/<int:group_id>/addFields', views.createAddFields, name='createAddFields')
]