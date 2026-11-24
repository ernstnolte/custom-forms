import json
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Form, FormGroup, FormField, FilledForm, FilledFormField, Option, OptionFormField
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST


def parse_json_body(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    return data if isinstance(data, dict) else None


@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})


## Returns json response of all forms (brief)
def getForms(request):
    data = list(Form.objects.values("id", "name", "description"))
    return JsonResponse({"success": True, "data": data})


## Returns json response a single form's details/attributes
def getFormDetail(request, form_id):
    # Get form from pk
    form = get_object_or_404(Form, pk=form_id)

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
def getFormResponses(request, form_id):
    form = get_object_or_404(Form, pk=form_id)
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
def getResponseDetail(request, filled_form_id):
    response = get_object_or_404(FilledForm, pk=filled_form_id)

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

## Receives new form data from client and creates a record
## Returns success message and form id, OR error message
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


## Receives new form group from client and form pk and creates record
## Returns success message and group id, OR error message
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


## Receives new form fields from client and group pk and creates record
## Returns success message and field id set, OR error message
@csrf_exempt
def createAddFields(request, group_id):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    try:
        data = json.loads(request.body)
        group = get_object_or_404(FormGroup, pk=group_id)
        created_fields = []

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
            created_fields.append({
                "id": field.id,
                "name": field.name
            })

        return JsonResponse({"success":True, "fields":created_fields})

    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)


## Receives new options from client and field pk and creates records
## Returns success message and option id set, OR error message
@csrf_exempt
def createAddOptions(request, field_id):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    try:
        data = json.loads(request.body)
        form_field = get_object_or_404(FormField, pk=field_id)
        created_options = []

        for option_data in data.get("options", []):
            option = Option.objects.create(
                name=option_data.get("name"),
            )
            OptionFormField.objects.create(
                form_field=form_field,
                option=option,
            )
            created_options.append({
                "id": option.id,
                "name": option.name
            })
        return JsonResponse({"success":True, "options":created_options})

    except Exception as ex:
            return JsonResponse({"success":False, "error":str(ex)}, status=500)

## Receives a filled form response from client and creates a record
## Returns success message and filled form id
def createFilledForm(request, form_id):
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
    
## Receives a form id from client and removes a record
## Returns a success message and form id, OR error message
def deleteForm(request, form_id):
    if request.method != "POST":
        return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)

    try:
        Form.objects.filter(pk=form_id).delete()
        return JsonResponse({"success":True, "form_id":form_id})
    
    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)


## Receives a group id from client and removes a record
## Returns a success message and group id, OR error message
@csrf_exempt
def deleteGroup(request, group_id):
    if request.method != "POST":
            return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    
    try:
        FormGroup.objects.delete(pk=group_id)
        return JsonResponse({"success":True, "group_id":group_id})
    
    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)


## Receives a field id from client and removes a record
## Returns a success message and field id, OR error message
@csrf_exempt
def deleteField(request, field_id):
    if request.method != "POST":
            return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    
    try:
        FormField.objects.delete(pk=field_id)
        return JsonResponse({"success":True, "field_id":field_id})
    
    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)


## Receives a filled form id from client and removes a record
## Returns a success message and form id, OR error message
@csrf_exempt
def deleteFilledForm(request, filled_form_id):
    if request.method != "POST":
            return JsonResponse({"success":False, "error":"Invalid request method"}, status=405)
    
    try:
        FilledForm.objects.delete(pk=filled_form_id)
        return JsonResponse({"success":True, "filled_form_id":filled_form_id})
    
    except Exception as ex:
        return JsonResponse({"success":False, "error":str(ex)}, status=500)

@csrf_exempt
def deleteOptionFormField(request, option_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

    try:
        OptionFormField.objects.filter(option_id=option_id).delete()
        return JsonResponse({"success": True, "option_id": option_id})

    except Exception as ex:
        return JsonResponse({"success": False, "error": str(ex)}, status=500)


@require_POST
def signup(request):
    data = parse_json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()

    if not username or not password:
        return JsonResponse(
            {"error": "username and password are required"},
            status=400,
        )

    User = get_user_model()
    candidate = User(username=username, email=email)

    try:
        validate_password(password, user=candidate)
    except ValidationError as error:
        return JsonResponse({"errors": error.messages}, status=400)

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
    except IntegrityError:
        return JsonResponse({"error": "That username is unavailable"}, status=409)

    return JsonResponse(
        {"success": True, "user": {"id": user.id, "username": user.get_username()}},
        status=201,
    )


@require_POST
def login_user(request):
    data = parse_json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = authenticate(
        request,
        username=data.get("username", ""),
        password=data.get("password", ""),
    )
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)

    login(request, user)  # Establishes the session and rotates the CSRF token.
    return JsonResponse({
        "success": True,
        "user": {"id": user.id, "username": user.get_username()},
        "csrfToken": get_token(request),
    })


@require_POST
def logout_user(request):
    logout(request)
    return JsonResponse({"success": True})