from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm
from .models import LQUser


class ProfileView(DetailView):
    """
    A view of the users profile. If no user is logged in propts user to create
    a profile
    """
    # TODO: create link to profile creation page
    # TODO: beautify profile and display user image
    model = LQUser
    template_name = 'UserProfile/profile.html'


class Login(TemplateView):
    """
    A form for logging a user into the app
    """
    template_name = 'UserProfile/login.html'


class UserNotFound(TemplateView):
    template_name = 'UserProfile/usernotfound.html'

class SignUp(FormView):
    """
    A form for signing a user up
    """
    template_name = 'UserProfile/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('map:map')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        if 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']
        user.save()
        auth_user(self.request)
        return super(SignUp, self).form_valid(form)


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
            url_redirect = reverse('profile:profile', kwargs={'pk':user.pk})
            return HttpResponseRedirect(url_redirect)
        else:
            # TODO: Inform user no longer active
            return HttpResponseRedirect(reverse('profile:notfound'))
    else:
        # TODO: Inform user login failed
        return HttpResponseRedirect(reverse('profile:notfound'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('map:map'))

def user_search(request):
    try:
        username = request.POST['username']
        user = LQUser.objects.get(username=username)
        return HttpResponseRedirect(reverse('profile:profile', kwargs={'pk':user.pk}))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('profile:notfound'))