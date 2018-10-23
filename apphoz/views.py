from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
import django.shortcuts

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse

from d.settings_common import JSON_TEMPLATE


def template(request):
    return JsonResponse(JSON_TEMPLATE)


def health(request):
    return HttpResponse('')


@login_required
def index(request):
    st = None
    try:
        sa = SocialAccount.objects.get(user=request.user)
        st = SocialToken.objects.get(account=sa)
    except Exception as e:
        pass
    return django.shortcuts.render(request, 'index.j2', { 'st' : st })