from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mmm_app.models import *

def landing(request):
    if request.user.is_authenticated():
        # get user info
        userInfo = UserInfo.objects.get(user=request.user)
        # set loggined
        loggined = True
    else:
        # set not loggined
        loggined = False
    
    # get all proejcts
    projects = Project.objects.all().order_by('-date_posted')
    # get all tags
    tags = Tag.objects.all().order_by('term')

    # render()
    

def userlogin(request):
    # render()

@login_required
def profile(request):
    userInfo = UserInfo.objects.get(user=request.user)
    if userInfo.is_sponsor:
        # query sponsor info
    if userInfo.is_developer:
        # query developer info

@login_required
def settings(request):
    

@login_required
def new_project(request):
    

@login_required
def edit_project(request, proj_id):
    

def view_project(request, proj_id):
    

def gallery(request):
