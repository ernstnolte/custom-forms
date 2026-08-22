import json
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Form, FormGroup, FormField, FilledForm, FilledFormField, Option, OptionFormField


## Returns json response of all forms (brief)
def getForms(request):
    data = list(Form.objects.values("id", "name", "description"))
    return JsonResponse({"success": True, "data": data})


## Returns json response a single form's details/attributes
def getFormDetail(request, pk):
    # Get form from pk
    form = get_object_or_404(Form, pk=pk)

    # Prefetch groups, fields, and options
    groups = (
        FormGroup.objects.filter(form=form)
        .prefetch_related("formfield_set__optionformfield_set__option")
        .order_by("index")
    )

    # Build Json Response
    data =  {
        "id" : form.id,
        "name" : form.name,
        "description" : form.description,
        "creation_date" : form.creation_date,
        "change_date" : form.change_date,
        "groups" : []
    }

    for group in groups:
        group_data = {
            "id" : group.id,
            "name" : group.name,
            "index" : group.index,
            "fields" : []
        }

        for field in group.formfield_set.all().order_by("index"):
            field_data = {
                "id" : field.id,
                "name" : field.name,
                "index" : field.index,
                "is_optional" : field.is_optional,
                "field_type" : field.field_type,
                "options" : [
                    {"id":  of.option.id, "name": of.option.name}
                    for of in field.optionformfield_set.all()
                ]
            }
            group_data["fields"].append(field_data)

        data["groups"].append(group_data)
    return JsonResponse({"success": True, "data": data})


## Returns json response of filled forms by form pk (brief)
def getFormResponses(request, pk):
    form = get_object_or_404(Form, pk=pk)
    filledForms = (
         FilledForm.objects.filter(form=form)
         .order_by("date_filled")
    )

    data =  {
        "id" : form.id,
        "name" : form.name,
        "description" : form.description,
        "creation_date" : form.creation_date,
        "change_date" : form.change_date,
        "responses" : []
    }

    for response in filledForms:
        response_data = {
            "id" : response.id,
            "date_filled" : response.date_filled,
            "filled_by" : f"{response.filled_by.first_name} {response.filled_by.last_name}"
        }
        data["responses"].append(response_data)

    return JsonResponse({"success": True, "data": data})


## Returns json response of a specific form response's details
def getResponseDetail(request, pk):
    response = get_object_or_404(FilledForm, pk=pk)

    groups = (
        FormGroup.objects.filter(form=response.form)
        .prefetch_related("formfield_set__optionformfield_set__option")
        .order_by("index")
    )

    answers_by_field = {
        answer.form_field_id: answer
        for answer in FilledFormField.objects.filter(filled_form=response)
        .select_related("selected_option")
    }

    def extract_answer(answer):
        if answer is None:
            return None
        if answer.text_value is not None:
            return answer.text_value
        if answer.numeric_value is not None:
            return answer.numeric_value
        if answer.date_time_value is not None:
            return answer.date_time_value
        if answer.selected_option is not None:
            return {
                "selected_option" : answer.selected_option.id,
                "selected_option_name" : answer.selected_option.name
            }
        if answer.is_checked is not None:
            return answer.is_checked
        return None

    data = {
        "form_id": response.form.id,
        "form_name": response.form.name,
        "date_filled": response.date_filled,
        "filled_by": (
            f"{response.filled_by.first_name} {response.filled_by.last_name}".strip()
            if response.filled_by
            else None
        ),
        "groups": [],
    }

    for group in groups:
        group_data = {
            "id": group.id,
            "name": group.name,
            "index": group.index,
            "fields": [],
        }

        for field in group.formfield_set.all().order_by("index"):
            answer = answers_by_field.get(field.id)
            group_data["fields"].append({
                "id": field.id,
                "question": field.name,
                "index": field.index,
                "is_optional": field.is_optional,
                "field_type": field.field_type,
                "options": [
                    {"id": of.option.id, "name": of.option.name}
                    for of in field.optionformfield_set.all()
                ],
                "answer": extract_answer(answer),
            })

        data["groups"].append(group_data)

    return JsonResponse({"success": True, "data": data})

def cast_answer(field_type, answer):
    """
    Casts a string answer into the correct type based on field_type.
    Returns a tuple: (text_value, numeric_value, date_time_value, is_checked, selected_option_id)
    """
    if answer is None:
        return None, None, None, None, None

    if field_type in ["text", "textarea"]:
        return answer, None, None, None, None

    if field_type == "number":
        try:
            return None, float(answer), None, None, None
        except ValueError:
            return None, None, None, None, None

    if field_type == "datetime":
        return None, None, parse_datetime(answer), None, None

    if field_type == "checkbox":
        return None, None, None, answer.lower() in ["true", "1", "yes"], None

    if field_type in ["radio", "itemchoice"]:
        try:
            return None, None, None, None, int(answer)  # option id
        except ValueError:
            return None, None, None, None, None

    return None, None, None, None, None

## Receives a filled form response from client and creates a record
## Returns success message and filled form id
def sendResponse(request, form_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        form = get_object_or_404(Form, pk=form_id)

        filled_form = FilledForm.objects.create(
            form=form,
            date_filled=timezone.now(),
            filled_by=request.user if request.user.is_authenticated else None
        )

        for field_data in data.get("fields", []):
            field_id = field_data.get("field_id")
            answer = field_data.get("answer")

            form_field = get_object_or_404(FormField, pk=field_id)

            text_value, numeric_value, date_time_value, is_checked, selected_option_id = cast_answer(
                form_field.field_type, answer
            )

            selected_option = None
            if selected_option_id:
                selected_option = get_object_or_404(Option, pk=selected_option_id)

            FilledFormField.objects.create(
                filled_form=filled_form,
                form_field=form_field,
                text_value=text_value,
                numeric_value=numeric_value,
                date_time_value=date_time_value,
                is_checked=is_checked,
                selected_option=selected_option
            )

        return JsonResponse({"success": True, "id": filled_form.id})

    except Exception as ex:
        return JsonResponse({"success": False, "error": str(ex)}, status=500)


## Receives new form data from client and creates a record
## Returns success message and form id
@csrf_exempt
def createForm(request):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        form = Form.objects.create(
            name=data.get("name"),
            description=data.get("description"),
            creation_date = timezone.now(),
            change_date = None
        )
        return JsonResponse({"success": True, "id": form.id})
    
    except Exception as ex:
        return JsonResponse({"success": False, "error": str(ex)}, status=500)


## Receives new form group from client and creates record
## Returns success message and group id OR error message
@csrf_exempt
def createAddGroup(request, form_id):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        form = get_object_or_404(Form, pk=form_id)
        group = FormGroup.objects.create(
            form=form,
            name=data.get("name"),
            index=data.get("index")
        )
        return JsonResponse({"success":True, "id":group.id})

    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)


## Receives new form field from client and creates record
## Returns success message and field id OR error message
@csrf_exempt
def createAddFields(request, group_id):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    try:
        data = json.loads(request.body)
        group = get_object_or_404(FormGroup, pk=group_id)

        # for fields in group
        for field_data in data.get("fields", []):
            if field_data.get("field_type") not in [choice[0] for choice in FormField.FIELD_TYPE_CHOICES]:
                        return JsonResponse({"success":False, "error":"field_type not in FIELD_TYPE_CHOICES"})
            
            field = FormField.objects.create(
                        form_group=group,
                        name=field_data.get("name"),
                        field_type=field_data.get("field_type"),
                        index=field_data.get("index"),
                        is_optional=field_data.get("is_optional")
                    )

        return JsonResponse({"success":True})

    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)


def createAddOptions(request, field_id):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    try:
        data = json.loads(request.body)
        field = get_object_or_404(FormField, field_id)

        for option_data in data.get("options", []):
            option = Option.objects.add(
                name=option_data.get("name"),
            )
            OptionFormField.objects.add(
                field=field,
                option=option,
            )

        return JsonResponse({"success":True})

    except Exception as ex:
            return JsonResponse({"success":False, "error":str(ex)}, status=500)