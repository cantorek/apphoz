from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
import django.shortcuts

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse

from apphoz.vcs import Vcs
from d.settings_common import JSON_TEMPLATE


def template(request):
    return JsonResponse(JSON_TEMPLATE)


def health(request):
    return HttpResponse('')


def index(request):
    return HttpResponse('')

@login_required
def profile(request):
    vcs = Vcs(request.user)

    return django.shortcuts.render(request, 'profile.html', { 'vcs' : vcs })