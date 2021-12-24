from BlogApp.models import POST
from django import template
from django.db.models import Count
register=template.Library()

@register.simple_tag
def total_posts():
    return POST.objects.count()

@register.inclusion_tag('testapp/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts=POST.objects.order_by('-publish')[:4]
    return{'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return POST.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
