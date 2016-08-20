from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404,HttpResponseRedirect
from .forms import *
# Create your views here.


def post_list(request):

    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('publish_date')

    content={
        'posts': posts,
    }
    return render(request,'blog/post_list.html', content )

def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    content={
        'post': post,
    }
    return render(request,'blog/post_detail.html', content)

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.publish_date = timezone.now()
            post.save()
            return HttpResponseRedirect(request,'blog/post_detail.html', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html',{'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.publish_date = timezone.now()
            post.save()
            return HttpResponseRedirect(request, 'blog/post_detail.html', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})



def post_draft_list(request):
    posts = Post.objects.filter(publish_date__isnull=True).order_by('created_date')
    content={
        'posts': posts,
    }
    return render(request, 'blog/post_draft_list.html',content)

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return HttpResponseRedirect(request,'blog/post_detail.html', pk=pk)


def post_remove(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return HttpResponseRedirect(request,'blog/post_list.html')