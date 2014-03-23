from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from models import *
from forms import *
import hashlib

HOMEPAGE_URL = '/'
LOGIN_URL = '/login_form/'
REGISTER_URL = '/register_form/'

def landing(request):
	if request.user.is_authenticated():
        # get user info
		userInfo = UserInfo.objects.get(user=request.user)
        # set loggined
		loggined = True
	else:
        # set not loggined
		loggined = False
    		
    # get all tags
	category_subs = Category_sub.objects.all().order_by('category_top')
	category_top_list = Category_top.objects.all().order_by('name')
	category_list = []
	for category_top in category_top_list:
		category = {}
		category['category_top'] = category_top
		category['category_sub_list'] = Category_sub.objects.filter(category_top=category_top)
		category_list.append(category)

    # category_sub = Category_sub.objects.all().order_by('name')
    
    # get list of projects
	projects = Project.objects.filter(status='OP').order_by('-date_posted')
    
    # apply filters
    #if request.method == 'POST':
    #	if filter0: # corresponds to checkbox being checked
    #		f0 = Category_sub.objects.get(name='filter0')
    #		projects.filter(Category_subs=f0)
    #	if filter1:
	#		f1 = Category_sub.objects.get(name='filter1')
	#		projects.filter(Category_subs=f1
	
	return render(request, 'landing.html', {'current': 'home', 'loggined': loggined, 'projects': projects, 'category_list': category_list, 'category_subs': category_subs})

# def user_register_form(request):
#     if request.method == 'GET':
#         if request.GET.get('next'):
#             next = request.GET['next']
#         else:
#             next = HOMEPAGE_URL
#         if request.user.is_authenticated():
#             return redirect(next)
#         else:
#             return render(request, 'register_form.html', {'next': next})
#     else:
#         return redirect(REGISTER_URL)

def user_register(request):
    if request.method == 'POST':
        uniqname = request.POST['uniqname']
        password = request.POST['password']
        if not (password and uniqname):
            return render(request, 'register_form.html')
        if User.objects.filter(username=uniqname).exists():
            return render(request, 'register_form.html')
        # TODO: Check legitimate username, password, uniqname, etc.
        email = uniqname + '@umich.edu'
        user = User.objects.create_user(username=uniqname, password=password, email=email)
        user.is_active = False
        send_verify_email(request, uniqname, email)
        user.save()
        return redirect('/thankyou/')
    else:
        return redirect(REGISTER_URL)

def send_verify_email(request, username, email):
    activation_code = generate_actication_code(username)
    send_mail('User Verification', request.build_absolute_uri('/activate/' + username + '/' + activation_code), 'mmm.umich@gmail.com', [email], fail_silently=False)

def user_activate(request, username, activation_code):
    if activation_code == generate_actication_code(username):
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        userInfo = UserInfo(user=user, is_sponsor=False, is_developer=False, setting_0=False, setting_1=False, setting_2=False)
        userInfo.save()
        return redirect(LOGIN_URL)
    else:
        return redirect(REGISTER_URL)

def generate_actication_code(username):
    return hashlib.sha256(username[0] + username[-1] + username).hexdigest()

def user_login_form(request):
    if request.method == 'GET':
        if request.GET.get('next'):
            next = request.GET['next']
        else:
            next = HOMEPAGE_URL
        if request.user.is_authenticated():
            return redirect(next)
        else:
            return render(request, 'login.html', {'next': next})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.POST['next']:
            next = request.POST['next']
        else:
            next = HOMEPAGE_URL
        if not (username and password):
            return render(request, 'login.html', {'next': next, 'username': username, 'error': 'Fields cannot be empty'})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(next);
            else:
                # Return a 'disabled account' error message
                return render(request, 'login.html', {'next': next, 'username': username, 'error': 'Account Disabled!'})
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html', {'next': next, 'username': username, 'error': 'Login Invalid'})
    else:
        return redirect(LOGIN_URL)

def user_logout(request):
    logout(request)
    # redirect to homepage
    return redirect(HOMEPAGE_URL)

@login_required
def profile_form(request, prof_id):
    if request.method == 'GET':
    # get info
    	userInfo = UserInfo.objects.get(user=prof_id)
        # render form
    	return render(request, 'profile.html', {'userInfoObj': userInfo})
    else: #if request.method == 'POST':
    # make edits to db with form values
    	User.objects.get(user=request.user).update(first_name=x)
    		#more user stuff
    	UserInfo.objects.get(user=request.user).update(setting_0 =x)
    		#more userinfo stuff
    	
    	# redirect to same page but with a GET method
    	return HttpResponseRedirect(PROFILE_FORM_URL)

@login_required
def update_profile(request):
   
    # redirect to profile form
    return redirect(PROFILE_FORM_URL)

@login_required
def settings_form(request): # merge with profile?
    # userInfo = UserInfo.objects.get(user=request.user)
    # return render()
    pass

@login_required
def update_settings(request): # merge with profile?
    pass

# @login_required
# def new_project_form(request):
#     userInfo = UserInfo.objects.get(user=request.user)
#     tags = Category_sub.objects.all().order_by('top')
#     # render()

@login_required
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = Project(
                            title=form.cleaned_data['title'], 
                            sponsor=request.user, 
                            status='OP', 
                            show_in_gallery=True, 
                            description=form.cleaned_data['description'], 
                            flags=0,
                        )
            project.save()
            project.image=request.FILES['image']
            for category_sub in form.cleaned_data['category_subs']:
                project.category_subs.add(category_sub)
            project.save()
            return redirect(HOMEPAGE_URL)
        else:
            print 'not valid'
    else:
        return redirect(HOMEPAGE_URL)


@login_required
def project_form(request, proj_id):
    try:
        project = Project.objects.get(id=proj_id)
    except Project.DoesNotExist:
        raise Http404
    category_subs = project.category_subs.all()
    comments = Comment.objects.filter(project=project)
    return render(request, 'projDetails.html', {'project': project, 'category_subs': category_subs, 'comments': comments})

@login_required
def apply_project(request):
    if request.method == 'POST':
        if request.POST['message'] and request.POST['proj_id']:
            message = request.POST['message']
            proj_id = request.POST['proj_id']
            applier = request.user
            try:
                project = Project.objects.get(id=proj_id)
            except Project.DoesNotExist:
                raise Http404
            profile_url = request.build_absolute_uri('/profile/' + str(applier.id) + '/')
            project_url = request.build_absolute_uri('/project/' + str(proj_id) + '/')
            sponsor_email = EmailMessage('Project Application on Michigan Mobile Manufactory', render(request, 'email_sponsor.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url}).content, 'mmm.umich@gmail.com', [project.sponsor.email], [], headers = {'Reply-To': applier.email})
            sponsor_email.send(fail_silently=False)
            applier = EmailMessage('Confirmation of Project Application on Michigan Mobile Manufactory', render(request, 'email_applier.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url}).content, 'mmm.umich@gmail.com', [applier.email], [])
            applier.send(fail_silently=False)
            return redirect(HOMEPAGE_URL)
        else:
            return redirect(HOMEPAGE_URL)
    else:
        return redirect(HOMEPAGE_URL)
    
@login_required
def edit_project(request, proj_id):
    projectInfo = Project.obejcts.get(id=proj_id)
    developers = proejctInfo.developers.all()
    tags = projectInfo.category_subs.all().order_by('top')
    comments = Comment.objects.filter(project=proj_id)

    # render()

def gallery(request):
	pass


