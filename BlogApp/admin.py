from django.contrib import admin
from BlogApp.models import POST,Comment
class POSTADMIN(admin.ModelAdmin):
    list_diaplay=['title','slug','author','body','publish','created','updated','status']
    prepopulated_fields={'slug':('title',)}
    list_filter=('status','author','created','publish')
    search_fields=('title','body')
    raw_id_fields=('author',)
    date_hierarchy='publish'
    ordering=['status','publish']



class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','body','created','updated','active','post']
    list_filter=['active','created','updated']
    search_fields=('name','email','body')




# Register your models here.
admin.site.register(POST,POSTADMIN)
admin.site.register(Comment,CommentAdmin)
