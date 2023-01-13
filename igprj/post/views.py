from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse

from post.models import Post, Tag, Follow, Stream, Likes
from comment.models import Comment
from comment.forms import NewCommentForm
from django.contrib.auth.models import User
from post.forms import NewPostform
from django.core.paginator import Paginator
from authy.models import Profile
from directs.models import Message

# Create your views here.
@login_required
def index(request):
    user=request.user
    m=Message.get_message(user)
    all_users=User.objects.all()
    follow_status=Follow.objects.filter(following=user, follower=request.user).exists()
    profile=Profile.objects.all()
    posts=Stream.objects.filter(user=user)
    group_ids=[]
    al_likes=Likes.objects.filter(user=user)
    all_likes=[]
    for i in al_likes:
        all_likes.append(i.post.id)
    all_favourite=[]
    profile=Profile.objects.get(user=user)
    for i in list(profile.favourite.all()):
        all_favourite.append(i.id)
    for post in posts:
        group_ids.append(post.post_id)
    post_items=Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    query=request.GET.get('q')
    if query:
        users=User.objects.filter(username__icontains=query)
        paginator=Paginator(users, 6)
        page_number=request.GET.get('page')
        users_paginator=paginator.get_page(page_number)

        return render(request, 'search.html',{'users':users,'query':query})
    
    context={
        'post_items':post_items,
        'follow_status':follow_status,
        'profile':profile,
        'all_users':all_users,
        'all_likes':all_likes,
        'all_favourite':all_favourite
    }
    return render(request, 'index.html', context)

@login_required
def NewPost(request):
    user=request.user
    profile=get_object_or_404(Profile, user=user)
    tags_obj=[]

    if request.method=="POST":
        form=NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture=form.cleaned_data.get('picture')
            caption=form.cleaned_data.get('caption')
            tag_form=form.cleaned_data.get('tags')
            tag_list=list(tag_form.split(','))

            for tag in tag_list:
                t, created=Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created=Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('profile', request.user.username)

    else:
        form=NewPostform
    context={'form':form}
    return render(request, 'newpost.html', context)

@login_required
def PostDetail(request, post_id):
    user=request.user
    post=get_object_or_404(Post,id=post_id)
    comments=Comment.objects.filter(post=post).order_by('-date')
    # user_like_list=Likes.objects.filter(post=post)
    # print(user_like_list)
    # for i in user_like_list:
    #     print(i.user.username)
    al_likes=Likes.objects.filter(user=user)
    all_likes=[]
    for i in al_likes:
        all_likes.append(i.post.id)
    all_favourite=[]
    profile=Profile.objects.get(user=user)
    for i in list(profile.favourite.all()):
        all_favourite.append(i.id)
    if request.method=="POST":
        form=NewCommentForm(request.POST)
        if form.is_valid():
            # form.save(post=post, user=user)
            print(request.POST['body'])
            c=Comment(user=user, body=request.POST['body'], post=post)
            c.save()
        #     comment=form.save(commit=False)
        #     comment.post=post
        #     comment.user=user
        #     comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form=NewCommentForm()
        
    context={
        'post':post,'form':form,'comments':comments,'all_likes':all_likes,'all_favourite':all_favourite
    }
    return render(request, 'postdetail.html', context)

@login_required
# def like(request, post_id):
#     user=request.user
#     post=Post.objects.get(id=post_id)
#     current_likes=post.likes
#     liked=Likes.objects.filter(user=user, post=post).count()

#     if not liked:
#         Likes.objects.create(user=user, post=post)
#         current_likes=current_likes + 1
#     else:
#         Likes.objects.filter(user=user, post=post).delete()
#         current_likes=current_likes-1
    
#     post.likes=current_likes
#     post.save()
#     return redirect(request.META.get('HTTP_REFERER'))

def like(request):
    user=request.user
    print(request.GET)
    post_id=request.GET.get('postid')
    post=Post.objects.get(id=post_id)
    current_likes=post.likes
    liked=Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes=current_likes + 1
        l=True

    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes=current_likes-1
        l=False
    
    post.likes=current_likes
    post.save()
    return JsonResponse({'status':'Data Saved',"current_likes":current_likes,'l':l})

@login_required
def favourite(request, post_id):
    user=request.user
    post=Post.objects.get(id=post_id)
    profile=Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def Tags(request, tag_slug):
    tag=get_object_or_404(Tag, slug=tag_slug)
    # print(tag)
    posts=Post.objects.filter(tags=tag).order_by('-posted')
    query=request.POST.get('q')
    result=True
    if query:
        if "#" in query:
            query=query[1:]
        try:
            tag=get_object_or_404(Tag, title=query)
            result=True
        except:
             result=False
        posts=Post.objects.filter(tags=tag).order_by('-posted')
        paginator=Paginator(posts, 6)
        page_number=request.GET.get('page')
        users_paginator=paginator.get_page(page_number)
        context={
        'posts':posts, 'tag':tag,'result':result
        }
        return render(request, 'tag.html',context)

    context={
        'posts':posts, 'tag':tag, 'result':result
    }
    return render(request, 'tag.html', context)

@login_required
def delete(request, post_id):
    del_post=Post.objects.get(id=post_id).delete()
    return redirect('profile',request.user.username)