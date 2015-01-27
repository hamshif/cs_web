
import os, sys, traceback, json, psycopg2, shutil, multiprocessing, csv

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


from django.middleware import csrf
from django.views.decorators.csrf import csrf_protect


from cs_res.util import respond_html

def home(request):

    return respond_html(request, "/cs_web/templates/cs_web/home.html")
