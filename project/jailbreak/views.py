import datetime

from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, Http404

from utilities.utils import create_form


def home(request, template=None):
    '''Home page'''
    context = RequestContext(request)

    context['home_page'] = True
    return render_to_response(template, context_instance=context)