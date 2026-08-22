from django.contrib import admin
from .models import Form, FormGroup, FormField, FilledForm, FilledFormField, Option, OptionFormField

# Register your models here.
@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_date', 'change_date')
    list_filter = ('creation_date',)
    search_fields = ('name', 'creation_date')

@admin.register(FormGroup)
class FormGroupAdmin(admin.ModelAdmin):
    list_display = ('form', 'name', 'index')
    list_filter = ('form', 'index')
    search_fields = ('form', 'name')

@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ('form_group', 'name', 'field_type', 'index', 'is_optional')
    list_filter = ('form_group', 'name', 'field_type', 'is_optional')
    search_fields = ('name',)

@admin.register(FilledForm)
class FormResponses(admin.ModelAdmin):
    list_display = ('form', 'filled_by', 'date_filled')
    list_filter = ('form', 'filled_by', 'date_filled')
    search_fields = ('form', 'filled_by', 'date_filled')

@admin.register(FilledFormField)
class FormResponseDetail(admin.ModelAdmin):
    list_display = ('filled_form', 'form_field')

@admin.register(Option)
class OptionAdminField(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(OptionFormField)
class OptionFormFieldAdmin(admin.ModelAdmin):
    list_display = ('form_field','option')