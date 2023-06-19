from datetime import time
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import *
from blogs.models import Post
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.core.mail import send_mail
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate, get_user_model, login, logout
# Create your views here.
def forum(request):
    posts = ForumPost.objects.all()
    blogposts = Post.objects.all()
    # comments = ForumComment.object.filter(post = posts)
    # posts.
    return render(request, 'forum.html',{'posts':posts, 'blogposts':blogposts[:10]})


def blog_post(request, post_id):
    if(request.method == 'POST'):
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        print(request.POST.get('csrfmiddlewaretoken'))
        user = request.user
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        parent = request.POST.get('parent')
        print('............',parent)
        post = ForumPost.objects.filter(sno = post_id).first()
        if(parent != ""):
            parent_comment = ForumComment.objects.filter(sno = int(parent)).first()
            obj=ForumComment(parent=parent_comment, user = user, message = message, subject=subject, post=post)
        else:
            obj=ForumComment(user = user, message = message, subject=subject, post=post)
        obj.save()
        email = user.email
        send_mail(
            'Someone Commented'+subject,
            'from:' +email +'\nmessage:\n'+message,
            'rk7305758@gmail.com',
            ['paliwalap7@gmail.com'],
            fail_silently=True,
            )

        comments = ForumComment.objects.filter(post = post, parent = None)
        replies = ForumComment.objects.filter(post = post).exclude(parent = None)

        repliesdict  = {}
        for i in replies:
            if i.parent not in repliesdict.keys():
                repliesdict[i.parent] = [i]
            else:
                repliesdict[i.parent].append(i)
        print(repliesdict)
        context = {'comments':comments, 'repliesdict':repliesdict,'post_details':post}

        html = render_to_string('forum-comment.html', context, request=request)
        return JsonResponse({'html':html})


    post = ForumPost.objects.filter(sno = post_id).first()
    recent_posts = ForumPost.objects.all()[:4:-1]
    # tags = Tags.objects.filter(forumpost=post)
    comments = ForumComment.objects.filter(post = post, parent=None)
    replies = ForumComment.objects.filter(post = post).exclude(parent = None)

    repliesdict  = {}
    for i in replies:
        if i.parent not in repliesdict.keys():
            repliesdict[i.parent] = [i]
        else:
            repliesdict[i.parent].append(i)

    print(repliesdict)
    return render(request, 'forum-detail.html', {'post_details':post, 'recent_posts':recent_posts, 'comments':comments, 'repliesdict':repliesdict,})

# @login_required()
def new_post(request):
    if(request.method == "POST"):
        # dt = str(datetime.datetime.now())
        message = request.POST.get('message')
        img = request.FILES['image']
        # timestamp = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
        obj = ForumPost(content = message, author=request.user,thumbnail=img)
        obj.save()
    return render(request, 'write-post.html')

def forum_search(request):
    query = request.GET.get('search')
    posts = ForumPost.objects.filter(content__contains = query)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2)

    try:
        post_obj = paginator.page(page)
    except PageNotAnInteger:
        post_obj = paginator.page(1)
    except EmptyPage:
        post_obj = paginator.page(paginator.num_pages)

    return render(request, 'forum-search.html', {'post_obj':post_obj, 'results_count':posts.count(), 'query':query})
