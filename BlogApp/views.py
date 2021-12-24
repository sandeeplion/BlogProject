from django.shortcuts import render,get_object_or_404
from BlogApp.models import POST,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from BlogApp.forms import EmailSendForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
# Create your views here.
def post_list_view(request):#tag_slug=None):
    list_view=POST.objects.all()
    # tag=None
    # if tag_slug:
    #     tag=get_object_or_404(Tag,slug=tag_slug)
    #     list_view=list_view.filter(tags__in=[tag])
    paginator=Paginator(list_view,3)
    page_number=request.GET.get('page')
    try:
        list_view=paginator.page(page_number)
    except PageNotAnInteger:
        list_view=paginator.page(1)
    except EmptyPage:
        list_view=paginator.page(paginator.num_pages)
    return render(request,'testapp/list.html',{'list_view':list_view})
def post_detail_view(request,year,month,day,post):
    form=CommentForm()
    post=get_object_or_404(POST,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    # post_tags_ids=post.tags.values_list('id',flat=True)
    # similar_posts=POST.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
        else:
            form=CommentForm()
    return render(request,'testapp/post_detail.html',{'post':post,'comments':comments,'csubmit':csubmit,'form':form})

def mail_send_view(request,id):
    form=EmailSendForm()
    post=get_object_or_404(POST,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recommeneds you to read "{}"'.format(cd['name'],cd['email'],post.title)
            message='Read Post at:\n {}\n\n Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'SandeeptheLion@blog.com',[cd['to']])
            sent=True
        else:
            form=EmailSendForm()
    return render(request,'testapp/mail.html',{'post':post,'form':form,'sent':sent})
