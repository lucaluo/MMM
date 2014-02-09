from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *

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
    pass

@login_required
def profile(request):
    userInfo = UserInfo.objects.get(user=request.user)
    if userInfo.is_sponsor:
        # query sponsor info
        pass
    if userInfo.is_developer:
        # query developer info
        pass

    # render()

@login_required
def settings(request):
    pass

@login_required
def new_project(request):
    pass

@login_required
def edit_project(request, proj_id):
    pass

def view_project(request, proj_id):
    pass

def gallery(request):
	pass
