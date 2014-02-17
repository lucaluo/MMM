from django.contrib import admin
from django.contrib.auth.models import User

from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Category_top, Category_sub

# Register your models here.

# admin model base class
class userBaseAdmin(admin.ModelAdmin):
	def first_name(self, obj):
		u = obj.user
		return u.first_name
	
	def last_name(self, obj):
		u = obj.user
		return u.last_name
		
	def email(self, obj):
		u = obj.user
		return u.email
		
	def is_active(self, obj):
		u = obj.user
		return u.is_active
		
	def is_staff(self, obj):
		u = obj.user
		return u.is_staff

# UserInfo
class UserInfoAdmin(userBaseAdmin):
	fieldsets = (
		('User Information', {
			'fields': ('user', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_sponsor', 'is_developer',)
		}),
		('User Settings', {
			'fields': ('setting_0', 'setting_1', 'setting_2',)
		}),
	)
	
	readonly_fields = ('user','first_name', 'last_name', 'email', 'is_active', 'is_staff',)

admin.site.register(UserInfo, UserInfoAdmin)

# Developer
class DeveloperAdmin(userBaseAdmin):
	fieldsets = (
		('Personal Information', {
			'fields': ('user', 'first_name', 'last_name', 'email',)
		}),
		('Profile Information', {
			'fields': ('image', 'major', 'bio', 'skills','projects',)
		}),
	)
	
	readonly_fields = ('user','first_name', 'last_name', 'email',)
	
admin.site.register(Developer, DeveloperAdmin)

# Sponsor
class SponsorAdmin(userBaseAdmin):
	fieldsets = (
		('Personal Information', {
			'fields': ('user', 'first_name', 'last_name', 'email',)
		}),
		('Organization Information', {
			'fields': ('org_name', 'image', 'org_bio', 'projects',)
		}),
	)
	
	readonly_fields = ('user','first_name', 'last_name', 'email',)
	
admin.site.register(Sponsor, SponsorAdmin)

# Project
class ProjectAdmin(admin.ModelAdmin):
	fieldsets = (
		('Project Information', {
			'fields': ('title', 'image',  'sponsor', 'date_posted', 'status', 'description', 'requirements', 'developers', 'category_tops', 'category_subs', 'show_in_gallery', 'flags',)
		}),
	)	
admin.site.register(Project, ProjectAdmin)

# Comment
class CommentAdmin(userBaseAdmin):
	fieldsets = (
		('Comment Information', {
			'fields': ('project', 'date_posted', 'title', 'text', 'flags',)
		}),
		('User Information', {
			'fields': ('user', 'first_name', 'last_name', 'email',)
		}),
	)
	
	readonly_fields = ('user', 'first_name', 'last_name', 'email',)
	
admin.site.register(Comment, CommentAdmin)

# Category_top
class Category_topAdmin(admin.ModelAdmin):
	readonly_fields = ('name',)
	fieldsets = (
		('Category Information', {
			'fields': ('name', 'category_subs',)
		}),
	)
admin.site.register(Category_top, Category_topAdmin)

# Category_sub
class Category_subAdmin(admin.ModelAdmin):
	fieldsets = (
		('Category Information', {
			'fields': ('top', 'name',)
		}),
	)
admin.site.register(Category_sub, Category_subAdmin)

