from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from .forms import SignUpForm


class ProfileView(TemplateView):
    """
    A view of the users profile. If no user is logged in propts user to create
    a profile
    """
    # TODO: create link to profile creation page
    # TODO: beautify profile and display user image
    template_name = 'UserProfile/profile.html'


class Login(TemplateView):
    """
    A form for logging a user into the app
    """
    template_name = 'UserProfile/login.html'


class CreateView(TemplateView):
    # TODO: create a page for creating a user profile
    pass


# from django docs
def auth_user(request):
    """
    Authenticates and logs in a user to the site using the username and
    password in POST.
    :param request:
    :return: HttpResponse
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('profile:profile'))
        else:
            # TODO: Inform user no longer active
            return HttpResponseRedirect(reverse('profile:login'))
    else:
        # TODO: Inform user login failed
        return HttpResponseRedirect(reverse('profile:login'))

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(user.password)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
    else:
        form = SignUpForm()
    return render(request, 'UserProfile/signup.html', {"form": form})
