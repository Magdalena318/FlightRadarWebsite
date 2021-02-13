from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from django.contrib.auth.hashers import check_password
from .validate import MinimumLengthValidator, NumberValidator, UppercaseValidator
from django.core.exceptions import ValidationError

#Registration
def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            response = redirect("/")
        else:
            form = RegisterForm()
            response = render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                result = {
                    'result': 'The registration has been unsuccessfull! A user with this username is already registered!'
                }
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                result = {
                    'result': 'The registration has been unsuccessfull! A user with this email is already registered!'
                }
            else:
                #Validate password
                validators = [MinimumLengthValidator, NumberValidator, UppercaseValidator]
                try:
                    for validator in validators:
                        validator().validate(form.cleaned_data['password'])
                except ValidationError as e:
                    result = {
                        'result': str(e)[2:-3]
                    }
                    return render(request, 'register.html', {'form': form, 'result': result})

                #Create user
                user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
                result = {
                    'success': 'The registration has been successfull!'
                }
        else:
            result = {
                'result': 'Form is invalid!'
            }
        response = render(request, 'register.html', {'form': form, 'result': result})
    else:
        result = {
            'result': 'Incorrect type of request'
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response


#Sign in
def sign_in(request):
    if request.user.is_authenticated:
        response = redirect("/")
    else:
        if request.method == 'GET':
            form = LoginForm()
            response = render(request, 'signin.html', {'form': form})
        elif request.method == 'POST':
            form = LoginForm(request.POST)
            print(form)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    response = redirect('/')
                else:
                    result = {
                        'failure': 'The username or password is incorrect!'
                    }
                    response = render(request, 'signin.html', {'form': form, 'result': result})
            else:
                result = {
                    'failure': 'Form is invalid!'
                }
                response = render(request, 'signin.html', {'form': form, 'result': result})
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = ChangePasswordForm()
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
            }
            response = render(request, 'change_password.html', {'form': form, 'data': data})
        elif request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
            }
            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                current_password = user.password
                entered_password = form.cleaned_data['old_password']
                if user.is_authenticated and check_password(entered_password, current_password):
                    # Validate password
                    validators = [MinimumLengthValidator, NumberValidator, UppercaseValidator]
                    try:
                        for validator in validators:
                            validator().validate(form.cleaned_data['new_password'])
                    except ValidationError as e:
                        result = {
                            'failure': str(e)[2:-3]
                        }
                        return render(request, 'change_password.html', {'form': form, 'result': result, 'data':data})

                    #Change password
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    result = {
                        'success': 'Your password has been changed successfully!'
                    }
                else:
                    result = {
                        'failure': 'The data entered is incorrect!'
                    }
            else:
                result = {
                    'failure': "Form is invalid!"
                }
            response = render(request, 'change_password.html', {'form': form, 'result': result, 'data':data})
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = render(request, 'result_auth.html', {'result': result})
    else:
        response = redirect("/")
    response.set_cookie("csrftoken", get_token(request))
    return response


def sign_off(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            logout(request)
            response = redirect("/")
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = render(request, 'result_auth.html', {'result': result})
    else:
        response = redirect("/")
    response.set_cookie("csrftoken", get_token(request))
    return response


def my_account(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'account_type': account_type,
            }
            response = render(request, 'my_account.html', {'data': data})
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = render(request, 'result.html', {'result': result})
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response
