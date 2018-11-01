import json
from pprint import pprint

import requests
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.decorators import login_required
import django.shortcuts

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from github import Github

from apphoz.utils import template_parameter
from .models import App, Language

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

@login_required
def create_app(request, repo_id):
    try:
        vcs = Vcs(request.user)
        g: Github = vcs.get_github()
        repo = g.get_repo(repo_id)

        app = App()
        app.name = repo.name
        app.template = django.conf.settings.JSON_TEMPLATE
        app.owner = request.user
        app.repo = repo.clone_url
        app.language = Language.objects.get(name=repo.language.lower())
        app.save()

        app.template['metadata']['name'] = '{0}-{1}'.format(app.name, app.date_added.strftime('%s'))

        template_parameter(app.template, 'NAME', app.name)
        template_parameter(app.template, 'IMAGE', app.language.__str__())
        template_parameter(app.template, 'SOURCE_REPOSITORY_URL', app.repo)
        template_parameter(app.template, 'GITHUB_WEBHOOK_SECRET', app.name)

        r = requests.post(
            'https://lb.wycislak.pl:8443/apis/template.openshift.io/v1/namespaces/oskarro-projekto/templateinstances',
            json.dumps(app.template),
            verify=False,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Connection': 'close',
                'Authorization': 'Bearer {0}'.format('jcwAQZmSO0QAT_QV8oAIKcbbT4O7mQ3SIAEJzzCwHxk'),
            })

        pprint(r.status_code)
        if r.status_code < 200 > 299:
            app.delete()
            raise Exception(r.text)

        app.save()

    except Exception as e:
        print(e)
        return django.http.response.HttpResponseNotFound(e)

    try:
        repo.create_hook(
            'web',
            {
                'url': 'https://lb.wycislak.pl:8443/apis/build.openshift.io/v1/namespaces/oskarro-projekto/buildconfigs/{0}/webhooks/{0}/github'.format(app.name),
                'content_type': 'json',
                'insecure_ssl': '1',
                'secret': app.name
            },
            events=['push'],
            active=True,
        )

    except Exception as e: #todo validate for hook exist exception
        pass

    return JsonResponse(json.loads(r.text))
