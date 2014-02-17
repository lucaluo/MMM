from django.contrib import admin
from django.contrib.auth.models import User

from mmm.mmm_app.models import UserInfo, Developer, Sponsor, Project, Comment, Category_top, Category_sub

# Register your models here.

# UserInfo
class UserInfoAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)
	fieldsets = (
		('User Information', {
			'fields': ('user', 'is_sponsor', 'is_developer',)
		}),
		('User Settings', {
			'fields': ('setting_0', 'setting_1', 'setting_2',)
		}),
	)
admin.site.register(UserInfo, UserInfoAdmin)

# Developer
class DeveloperAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)
	fieldsets = (
		('Developer Information', {
			'fields': ('user', 'image', 'major', 'bio', 'skills','projects',)
		}),
	)
admin.site.register(Developer, DeveloperAdmin)

# Sponsor
class SponsorAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)
	fieldsets = (
		('Sponsor Information', {
			'fields': ('user', 'org_name', 'image', 'org_bio', 'projects',)
		}),
	)
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
class CommentAdmin(admin.ModelAdmin):
	readonly_fields = ('user', 'project', 'date_posted',)
	fieldsets = (
		('Comment Information', {
			'fields': ('user', 'project', 'date_posted', 'title', 'text', 'flags',)
		}), 
	)
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

