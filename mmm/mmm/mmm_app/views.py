from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template import RequestContext
from models import *
from forms import *
import hashlib

HOMEPAGE_URL = '/'
LOGIN_URL = '/login/'
REGISTER_URL = '/login/'

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
	category_list = getAllCategories()
	
	# message color and contents
	mtype = 'none'
	mcontents = ''
	
	# get list of projects
	projects = Project.objects.filter(status='OP', approved=True).order_by('-date_posted')
	bookmarked = False
	f_cat_subs_dict = {}
	for x in category_list:
		for cs in x['category_sub_list']:
			f_cat_subs_dict[cs] = False
	af = ''
	
	# filtering on get method
	form = FilterForm(data=request.GET)

	if loggined and form.is_valid():
		# bookmarked projects
		b = form.cleaned_data['bookmarked']
		if b:
			projects = UserInfo.objects.get(user=request.user).bookmarks.all()
			bookmarked = True
	
		# checkbox filters
		f_cat_subs = form.cleaned_data['f_category_subs']
			
		for cat_sub in f_cat_subs:
			# corresponds to checkbox being checked
			projects = projects.filter(category_subs=cat_sub)
			f_cat_subs_dict[cat_sub] = True
		
		# search box
		af = form.cleaned_data['additional_filter']
		match = False
		if af:
			for cd in category_list:
				for cs in cd['category_sub_list']:
					if cs.name == af:
						projects = projects.filter(category_subs=cs)
						match = True
			if not match:
				newprojects = projects.filter(title__icontains=form.cleaned_data['additional_filter'])
				if not newprojects:
					projects = projects.filter(description__icontains=form.cleaned_data['additional_filter'])
				else:
					projects = newprojects
					
		if not projects:
			mtype = 'alert-danger'
			mcontents = 'No projects matched'
			
	elif loggined:
		mtype = 'alert-danger'
		mcontents = 'Invalid filters'
		projects = []
			
	return render(request, 'landing.html', {'filterForm': form, 'projects': projects, 'category_list': category_list, 'message_type': mtype, 'message_contents': mcontents, 'cat_sub_checked_dict': f_cat_subs_dict, 'bookmarked': bookmarked, 'additional_filter': af}, context_instance=RequestContext(request))

def getAllCategories():
	category_top_list = Category_top.objects.all().order_by('pk')
	category_list = []
	for category_top in category_top_list:
		category = {}
		category['category_top'] = category_top
		category['category_sub_list'] = Category_sub.objects.filter(category_top=category_top)
		category_list.append(category)
	return category_list

def user_register(request):
	if request.method == 'POST':
		uniqname = request.POST['uniqname']
		password = request.POST['password']
		full_name = request.POST['full_name']
		if not (password and uniqname and full_name):
			mtype = 'alert-danger'
			mcontents = 'Please fill all register fields!'
			return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		if User.objects.filter(username=uniqname).exists():
			mtype = 'alert-danger'
			mcontents = 'Uniqname has been registered!'
			return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		# TODO: Check legitimate username, password, uniqname, etc.
		email = uniqname + '@umich.edu'
		user = User.objects.create_user(username=uniqname, password=password, email=email)
		user.is_active = False
		user.save()
		userInfo = UserInfo(user=user, full_name=full_name, setting_0=False, setting_1=False, setting_2=False)
		userInfo.save()
		send_verify_email(request, uniqname, email)
		mtype = 'alert-success'
		mcontents = 'Please check your email for an activation link!'
		return render(request, 'login.html', {'username': uniqname, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
	else:
		return redirect(REGISTER_URL)

def send_verify_email(request, username, email):
	activation_code = generate_actication_code(username)
	verify_url = request.build_absolute_uri('/activate/' + username + '/' + activation_code)
	user = User.objects.get(username=username)
	userInfo = UserInfo.objects.get(user=user)
	send_mail('Michigan Mobile Manufactory User Verification', render(request, 'email_verification.txt', {'user': user, 'userInfo': userInfo, 'verify_url': verify_url}).content, 'mmm.umich@gmail.com', [email], fail_silently=False)

def user_activate(request, username, activation_code):
	if activation_code == generate_actication_code(username):
		user = User.objects.get(username=username)
		user.is_active = True
		user.save()
		return redirect(LOGIN_URL)
	else:
		return redirect(REGISTER_URL)

def generate_actication_code(username):
	return hashlib.sha256(username[0] + username[-1] + username).hexdigest()

def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		if request.POST.get('next'):
			next = request.POST['next']
		else:
			next = HOMEPAGE_URL
		if not (username and password):
			mtype = 'alert-danger'
			mcontents = 'Please fill your uniqname and password!'
			return render(request, 'login.html', {'next': next, 'username': username, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(next);
			else:
				mtype = 'alert-danger'
				mcontents = 'Account is not activated!'
				return render(request, 'login.html', {'next': next, 'username': username, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
		else:
			mtype = 'alert-danger'
			mcontents = 'The user does not exists!'
			return render(request, 'login.html', {'next': next, 'username': username, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
	else:
		if request.GET.get('next'):
			next = request.GET['next']
		else:
			next = HOMEPAGE_URL
		if request.user.is_authenticated():
			return redirect(next)
		else:
			return render(request, 'login.html', {'next': next}, context_instance=RequestContext(request))

def user_logout(request):
	logout(request)
	# redirect to homepage
	return redirect(HOMEPAGE_URL)

@login_required
def profile(request, prof_id):
	mtype = 'none'
	mcontents = ''
	if request.method == 'POST':
		if prof_id == str(request.user.id):
			# bound form
			form = ProfileForm(request.POST, request.FILES)
			if form.is_valid():
				try:
					# get user and userInfo to edit
					userInfo = UserInfo.objects.get(user=request.user)
				except UserInfo.DoesNotExist:
					raise Http404
					
				# this is the cleaned data
				full_name = form.cleaned_data['full_name']
				major = form.cleaned_data['major']
				bio = form.cleaned_data['bio']
				weekly_email = form.cleaned_data['weekly_email']
				# update models in db
				userInfo.full_name = full_name
				userInfo.major = major
				userInfo.bio = bio
				userInfor.weekly_email = weekly_email
				if request.FILES.get('image'):
					userInfo.image = request.FILES['image']
				try:
					userInfo.save()
					# message color and contents
					mtype = 'alert-success'
					mcontents = 'Profile successfully updated'
				except userInfo.DoesNotExist: # what other errors could occur?
					# message color and contents
					mtype = 'alert-danger'
					mcontents = 'Profile could not be updated'
				# get sponsored projects
				projects = Project.objects.filter(sponsor=prof_id)
				#return redirect('/profile/' + prof_id + '/')
				return render(request, 'profile.html', {'userInfoObj': userInfo, 'profileEditForm':form, 'projects': projects, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))
			else:
				mtype = 'alert-danger'
				mcontents = 'Edit is not valid!'
				print form.errors
		else:
			mtype = 'alert-danger'
			mcontents = 'User does not have permission to edit!'
			print request.user.id
	# GET request
	try:
		# get user and userInfo to edit
		userInfo = UserInfo.objects.get(user=request.user)
	except UserInfo.DoesNotExist:
		raise Http404
	# unbound form
	form = ProfileForm()
	# get info
	userInfo = UserInfo.objects.get(user=prof_id)
	# get sponsored projects
	projects = Project.objects.filter(sponsor=prof_id)
	# render
	return render(request, 'profile.html', {'userInfoObj': userInfo, 'profileEditForm':form, 'projects': projects, 'message_type': mtype, 'message_contents': mcontents}, context_instance=RequestContext(request))

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
							approved=False,
							description=form.cleaned_data['description'], 
							flags=0,
						)
			project.save()
			if request.FILES.get('image'):
				project.image = request.FILES['image']
			if request.POST.get('in_gallery'):
				project.show_in_gallery = True
			else:
				project.show_in_gallery = False
			for category_sub in form.cleaned_data['category_subs']:
				project.category_subs.add(category_sub)
			project.save()
			return redirect(HOMEPAGE_URL)
		else:
			print 'not valid'
			return redirect(HOMEPAGE_URL)
	else:
		return redirect(HOMEPAGE_URL)


@login_required
def project(request, proj_id):
	if request.method == 'POST':
		form = ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			if project.sponsor == request.user:
				project.title = form.cleaned_data['title']
				project.description = form.cleaned_data['description']
				if request.POST.get('status'):
					project.status = request.POST['status']
				if request.POST.get('in_gallery'):
					project.show_in_gallery = True
				else:
					project.show_in_gallery = False
				if request.FILES.get('image'):
					project.image = request.FILES['image']
				project.category_subs.through.objects.all().delete()
				for category_sub in form.cleaned_data['category_subs']:
					project.category_subs.add(category_sub)
				project.save()
				return redirect('/project/' + proj_id + "/")
			else:
				print 'no permission'
		else:
			print 'not valid'
	else: # GET
		try:
			project = Project.objects.get(id=proj_id)
		except Project.DoesNotExist:
			raise Http404
		sponsor = UserInfo.objects.get(user=project.sponsor)
		category_subs = project.category_subs.all()
		category_sub_ids = [category_sub.id for category_sub in category_subs]
		comments = Comment.objects.filter(project=project)
		commentsObj = []
		for comment in comments:
			commentObj = {'comment': comment, 'commenter': UserInfo.objects.get(user=comment.user)}
			commentsObj.append(commentObj)
		category_list = getAllCategories()
		if project in UserInfo.objects.get(user=request.user).bookmarks.all():
			is_bookmarked = True
		else:
			is_bookmarked = False
		return render(request, 'projDetails.html', {'project': project, 'sponsor': sponsor, 'category_subs': category_subs, 'commentsObj': commentsObj, 'category_list': category_list, 'category_sub_ids': category_sub_ids, 'is_bookmarked': is_bookmarked}, context_instance=RequestContext(request))

@login_required
def apply_project(request):
	if request.method == 'POST':
		if request.POST['message'] and request.POST['proj_id']:
			message = request.POST['message']
			proj_id = request.POST['proj_id']
			applier = request.user
			applierInfo = UserInfo.objects.get(user=applier)
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			sponsorInfo = UserInfo.objects.get(user=project.sponsor)
			profile_url = request.build_absolute_uri('/profile/' + str(applier.id) + '/')
			project_url = request.build_absolute_uri('/project/' + str(proj_id) + '/')
			sponsor_email = EmailMessage('Project Application on Michigan Mobile Manufactory', render(request, 'email_sponsor.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url, 'applierInfo': applierInfo, 'sponsorInfo': sponsorInfo}).content, 'mmm.umich@gmail.com', [project.sponsor.email], [], headers = {'Reply-To': applier.email})
			sponsor_email.send(fail_silently=False)
			applier = EmailMessage('Confirmation of Project Application on Michigan Mobile Manufactory', render(request, 'email_applier.txt', {'message': message, 'project': project, 'applier': applier, 'sponsor': project.sponsor, 'profile_url': profile_url, 'project_url': project_url, 'applierInfo': applierInfo, 'sponsorInfo': sponsorInfo}).content, 'mmm.umich@gmail.com', [applier.email], [])
			applier.send(fail_silently=False)
			return redirect(HOMEPAGE_URL)
		else:
			return redirect(HOMEPAGE_URL)
	else:
		raise Http404
	
# @login_required
# def edit_project(request, proj_id):
# 	projectInfo = Project.obejcts.get(id=proj_id)
# 	#developers = proejctInfo.developers.all()
# 	tags = projectInfo.category_subs.all().order_by('top')
# 	comments = Comment.objects.filter(project=proj_id)
# 	# render()

@login_required
def new_comment(request):
	if request.method == 'POST':
		if request.POST['comment'] and request.POST['proj_id']:
			comment = request.POST['comment']
			proj_id = request.POST['proj_id']
			try:
				project = Project.objects.get(id=proj_id)
			except Project.DoesNotExist:
				raise Http404
			comment = Comment(user=request.user, project=project, text=comment, flags=0)
			comment.save()
			return redirect('/project/' + str(proj_id))
		else:
			return redirect(HOMEPAGE_URL)
	else:
		raise Http404


@login_required
def delete_comment(request, proj_id, comm_id):
	try:
		comment = Comment.objects.get(id=comm_id)
		if str(comment.project.id) != proj_id:
			# TODO error message comment and proejct id not correspond
			print "comment and proejct id not correspond"
		elif comment.user != request.user:
			# TODO no permission to delete this comment
			print "no permission to delete this comment"
		else:
			comment.delete()
			return redirect('/project/' + proj_id + '/')
	except Comment.DoesNotExist:
		# TODO error message comment to delete not exists
		print "error message comment to delete not exists"

@login_required
def bookmark(request, proj_id):
	try:
		project = Project.objects.get(id=proj_id)
	except Project.DoesNotExist:
		raise Http404
	userInfo = UserInfo.objects.get(user=request.user)
	if project not in userInfo.bookmarks.all():
		userInfo.bookmarks.add(project)
	return redirect('/project/' + proj_id + '/')


@login_required
def unbookmark(request, proj_id):
	try:
		project = Project.objects.get(id=proj_id)
	except Project.DoesNotExist:
		raise Http404
	userInfo = UserInfo.objects.get(user=request.user)
	if project in userInfo.bookmarks.all():
		userInfo.bookmarks.remove(project)
	return redirect('/project/' + proj_id + '/')

def gallery(request):
	pass


