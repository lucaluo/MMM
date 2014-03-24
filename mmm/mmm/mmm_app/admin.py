from django.contrib import admin
from django.contrib.auth.models import User

from mmm.mmm_app.models import *

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
		
# Action for deleting flagged comments
def deleteFlagged_3plus(modeladmin, request, queryset):
	for obj in queryset:
		if obj.flags >= 3:
			obj.delete()
deleteFlagged_3plus.short_description = "Delete comments with 3 or more flags"

# Action for setting project status to open
def setStatusOpen(modeladmin, request, queryset):
	queryset.update(status='OP')
setStatusOpen.short_description = "Set project statuses to Open"
	
# Action for setting project status to open
def setStatusClosed(modeladmin, request, queryset):
	queryset.update(status='CL')
setStatusClosed.short_description = "Set project statuses to Closed"
	
# Action for setting project status to open
def setStatusComp(modeladmin, request, queryset):
	queryset.update(status='CO')
setStatusComp.short_description = "Set project statuses to Completed"

# Action for showing project in gallery
def setShowInGallery(modeladmin, request, queryset):
	queryset.update(show_in_gallery=True)
setShowInGallery.short_description = "Set show_in_gallery to True"
	
# inline class for editing sub categories
class CategorySubInline(admin.TabularInline):
	model = Category_sub

# UserInfo
class UserInfoAdmin(userBaseAdmin):
	fieldsets = (
		('Account Information', {
			'fields': ('user', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'setting_0', 'setting_1', 'setting_2',)
		}),
		('User Information', {
			'fields': ('full_name', 'major', 'bio', 'image',)
		}),
		('Bookmarked Projects', {
			'fields': ('bookmarks',)
		}),
	)
	
	readonly_fields = ('user','first_name', 'last_name', 'email', 'is_active', 'is_staff',)

	list_display = ('user', 'first_name', 'last_name',)
	
	search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'major', 'org_name']	
	
admin.site.register(UserInfo, UserInfoAdmin)


# Project
class ProjectAdmin(admin.ModelAdmin):
	fieldsets = (
		('Project Information', {
			'fields':('title', 'image', 'sponsor', 'status', 'description', 'category_subs', 'show_in_gallery', 'flags',)
		}), #'date_posted', doesn't work inexplicably
	)
	
	actions = [setStatusOpen, setStatusClosed, setStatusComp, setShowInGallery, deleteFlagged_3plus]
	
	search_fields = ['sponsor__username', 'sponsor__email', 'sponsor__first_name', 'sponsor__last_name', 'title', 'category_subs__name']
		
admin.site.register(Project, ProjectAdmin)

# Comment
class CommentAdmin(userBaseAdmin):
	fieldsets = (
		('Comment Information', {
			'fields': ('project', 'date_posted', 'text', 'flags',)
		}),
		('User Information', {
			'fields': ('user', 'first_name', 'last_name', 'email',)
		}),
	)
	
	readonly_fields = ('user', 'first_name', 'last_name', 'email',)
	
	list_display = ('project', 'user', 'flags',)
	
	search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'project__title']
	
	actions = [deleteFlagged_3plus]
	
admin.site.register(Comment, CommentAdmin)

# Category_top
class Category_topAdmin(admin.ModelAdmin):
	readonly_fields = ('name',)
	
	inlines = [CategorySubInline]
	
	fieldsets = (
		('Category Information', {
			'fields': ('name',)
		}),
	)
	
	search_fields = ['name']
admin.site.register(Category_top, Category_topAdmin)

# Category_sub
class Category_subAdmin(admin.ModelAdmin):
	fieldsets = (
		('Category Information', {
			'fields': ('category_top', 'name',)
		}),
	)
	
	list_display = ('name', 'category_top')
	
	search_fields = ['name', 'category_top__name']
	
admin.site.register(Category_sub, Category_subAdmin)

