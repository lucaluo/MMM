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
    tags = Category_sub.objects.all().order_by('top')

    # render()
    

def userlogin(request):
    # render()
    pass

@login_required
def profile(request):
    userInfo = UserInfo.objects.get(user=request.user)
    if userInfo.is_sponsor:
        # query sponsor info
        sponsorInfo = Sponsor.objects.get(user=request.user)
    else:
        sponsorInfo = []
    if userInfo.is_developer:
        # query developer info
        developerInfo = Developer.objects.get(user=request.user)
    else:
        developerInfo = []

    # render()

@login_required
def update_profile(request):
    # redirect()

@login_required
def settings(request):
    userInfo = UserInfo.objects.get(user=request.user)

    # render()

@login_required
def new_project(request):
    userInfo = UserInfo.objects.get(user=request.user)
    tags = Category_sub.objects.all().order_by('top')

    # render()

@login_required
def edit_project(request, proj_id):
    # redirect()
    
@login_required
def view_project(request, proj_id):
    projectInfo = Project.obejcts.get(id=proj_id)
    developers = proejctInfo.developers.all()
    tags = projectInfo.category_subs.all().order_by('top')
    comments = Comment.objects.filter(proejct=proj_id)

    # render()

def gallery(request):

