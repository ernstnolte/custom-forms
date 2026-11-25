# Credit to softwareideas.net Dynamic Form Model (ERD Example) - Dusan Rodina
# https://www.softwareideas.net/a/1510/dynamic-form-model-erd-example-

from django.db import models
from django.conf import settings

class Form(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    creation_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=False, default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class FormGroup(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    index = models.IntegerField()

    class Meta:
        unique_together = ('form', 'index')

    def __str__(self):
        return f"{self.form.name} - {self.name}"


class Option(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FormField(models.Model):
    TEXT = "text"
    CHECKBOX = "checkbox"
    NUMBER = "number"
    DATETIME = "datetime"
    TEXTAREA = "textarea"
    ITEMCHOICE = "itemchoice"
    RADIO = "radio"

    FIELD_TYPE_CHOICES = [
        (TEXT, "Text"),
        (CHECKBOX, "Check box"),
        (NUMBER, "Number"),
        (DATETIME, "DateTime"),
        (TEXTAREA, "Text Area"),
        (ITEMCHOICE, "Item Choice"),
        (RADIO, "Radio Buttion")
    ]

    form_group = models.ForeignKey(FormGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    index = models.IntegerField()
    is_optional = models.BooleanField(default=False)

    class Meta:
        unique_together = ('form_group', 'index')

    def __str__(self):
        return self.name


# associative table to join M:N relationship between FormField and Option
class OptionFormField(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('option', 'form_field')


class FilledForm(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    date_filled = models.DateTimeField()
    filled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='resources',
        null=True,
    )

    def __str__(self):
        return f"{self.form.name} - {self.date_filled} - {self.filled_by}"


class FilledFormField(models.Model):
    filled_form = models.ForeignKey(FilledForm, on_delete=models.CASCADE)
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE)

    is_checked = models.BooleanField(null=True)
    text_value = models.CharField(max_length=2000, null=True, blank=True)
    numeric_value = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
    date_time_value = models.DateTimeField(null=True, blank=True)
    selected_option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('filled_form', 'form_field')
