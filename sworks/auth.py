from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from sworks.forms import RegisterForm, LoginForm
from sworks.models import Student


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != form.cleaned_data["rep_password"]:
                messages.error(request, "пароли не совпадают")
                data = {'username': form.cleaned_data["username"],
                        'schooler_class': form.cleaned_data["schooler_class"],
                        'schooler_group': form.cleaned_data["schooler_group"],
                        'mail': form.cleaned_data["mail"],
                        'name': form.cleaned_data["name"],
                        'second_name': form.cleaned_data["second_name"],
                        }
                return render(request, "sworks/register.html", {
                    'form': RegisterForm(initial=data),
                    'ins_form': LoginForm()
                })
            else:
                musername = form.cleaned_data["username"]
                schooler_class = form.cleaned_data["schooler_class"]
                schooler_group = form.cleaned_data["schooler_group"]
                mmail = form.cleaned_data["mail"]
                name = form.cleaned_data["name"]
                second_name = form.cleaned_data["second_name"]
                mpassword = form.cleaned_data["password"]
                try:
                    user = User.objects.create_user(username=musername,
                                                    email=mmail,
                                                    password=mpassword)
                    if user:
                        user.first_name = name
                        user.last_name = second_name
                        user.save()
                        s = Student.objects.create(user=user, st_klass=schooler_class, st_group=schooler_group)
                        s.save()
                    return HttpResponseRedirect("/")
                except:
                    messages.error(request, "Такой пользователь уже есть")
                    data = {'username': form.cleaned_data["username"],
                            'schooler_class': form.cleaned_data["schooler_class"],
                            'schooler_group': form.cleaned_data["schooler_group"],
                            'mail': form.cleaned_data["mail"],
                            'name': form.cleaned_data["name"],
                            'second_name': form.cleaned_data["second_name"],
                            }
                    return render(request, "sworks/register.html", {
                        'form': RegisterForm(initial=data),
                        'ins_form': LoginForm()
                    })
        else:
            return HttpResponseRedirect("/register/")
    else:
        return render(request, "sworks/register.html", {
            'form': RegisterForm(),
            'login_form': LoginForm()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def index(request):
    if request.method == "POST":
        if ("username" in request.POST) and ("password" in request.POST):
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            request.POST._mutable = True
            if user is not None and user.is_active:
                # Правильный пароль и пользователь "активен"
                auth.login(request, user)
                messages.success(request, "успешный вход")
            else:
                messages.error(request, "пара логин-пароль не найдена")
    template = 'sworks/index.html'
    context = {
        "user": request.user,
        "login_form": LoginForm(),
    }
    return render(request, template, context)