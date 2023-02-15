from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from post_db.models import Posts, Post_votes
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
# Create your views here.

class IndexView(generic.ListView):
    template_name='post_db/index.html'
    context_object_name='latest_posts_list'

    def __str__(self):
        return self.post_title

    def get_queryset(self):
        """Return the last five published posts."""
        return Posts.objects.order_by('-pub_date')#[:5]

class DetailView(generic.DetailView):
    model = Posts
    template_name = 'post_db/detail.html'

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        post.views += 1
        post.save()
        return post

def post_detail(request, post_id):
    posts = Posts.objects.get(pk=post_id)
    upvoted = Post_votes.objects.filter(post_id=post_id, up_or_d=1).exists()
    downvoted = Post_votes.objects.filter(post_id=post_id, up_or_d=-1).exists()
    context = {
        'posts': posts,
        'upvoted': upvoted,
        'downvoted': downvoted,
    }
    return render(request, 'detail.html', context)

def upvote(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if Post_votes.objects.filter(post_id=pk):
        vote_check = Post_votes.objects.filter(post_id=pk).get()
        if vote_check.up_or_d == 1:
            post.views -= 1
            post.save()
            return redirect('post_db:detail', pk=pk)
        else:
            post.score += 2
            post.views -= 1
            vote_check.up_or_d = 1
            post.save()
            vote_check.save()
            return redirect('post_db:detail', pk=pk)
    else:
        vote_check = Post_votes(post_id=pk, user_id=1, up_or_d=1)
        post.score += 1
        post.views -= 1
        post.save()
        vote_check.save()
        return redirect('post_db:detail', pk=pk)

def downvote(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if Post_votes.objects.filter(post_id=pk).get():
        vote_check = Post_votes.objects.filter(post_id=pk).get()
        if vote_check.up_or_d == -1:
            post.views -= 1
            post.save()
            return redirect('post_db:detail', pk=pk)
        else:
            post.score -= 2
            post.views -= 1
            vote_check.up_or_d = -1
            post.save()
            vote_check.save()
            return redirect('post_db:detail', pk=pk)
    else:
        vote_check = Post_votes(post_id=pk, user_id=1, up_or_d=1)
        post.score -= 1
        post.views -= 1
        post.save()
        vote_check.save()
        return redirect('post_db:detail', pk=pk)

def create_post(request):
    post=None
    if request.method == 'POST':
        if request.POST.get('post_title') and request.POST.get('post_text'):
            post = Posts(post_title=request.POST.get('post_title'), post_text=request.POST.get('post_text') ,pub_date=timezone.localtime(timezone.now()))
            post.save()
            return redirect('post_db:index')
        else:
            message = "Please fill in all required fields."
            return render(request, 'post_db/create_post.html', {'post': post, 'message': message})
    else:
        return render(request, 'post_db/create_post.html')

def edit_post(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    if request.method == 'POST':
        if request.POST['post_title'] and request.POST['post_text']:
            post.post_title = request.POST['post_title']
            post.post_text = request.POST['post_text'] # replace 'new_text' with the name of your textarea input
#            post.pub_date=timezone.localtime(timezone.now())
            post.save()
            return redirect('post_db:detail', post_id)
        else:
            message = "Please fill in all required fields."
            return render(request, 'post_db/edit_post.html', {'post': post, 'message': message})
    else:
        return render(request, 'post_db/edit_post.html', {'post': post})

