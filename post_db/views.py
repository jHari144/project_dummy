from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from post_db.models import Posts, Post_votes, Replies
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['pk']
        context['Replys'] = Replies.objects.filter(parent_id=post_id).order_by('-pub_date')
        context['upvoted'] = Post_votes.objects.filter(post_id=post_id, up_or_d=1).exists()
        context['downvoted'] = Post_votes.objects.filter(post_id=post_id, up_or_d=-1).exists()

        return context

def post_detail(request, post_id):
    posts = Posts.objects.get(pk=post_id)
    upvoted = Post_votes.objects.filter(post_id=post_id, up_or_d=1).exists()
    downvoted = Post_votes.objects.filter(post_id=post_id, up_or_d=-1).exists()
    context = {
        'posts': posts,
        'upvoted': upvoted,
        'downvoted': downvoted,
    }
    return render(request, 'post_db/detail.html', context)

def upvote(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if Post_votes.objects.filter(post_id=pk).exists():
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
    if Post_votes.objects.filter(post_id=pk).exists():
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

def reply(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    reply=None
    if request.method == 'POST':
        if request.POST.get('reply_text'):
            reply = Replies(parent_id=post_id, user_id=1, reply_text=request.POST.get('reply_text'), pub_date=timezone.localtime(timezone.now()))
            post.no_replies += 1
            reply.save()
            post.save()
            return redirect('post_db:detail', post_id)
        else:
            message = "Please fill in all the required fields."
            return render(request, 'post_db/reply.html', {'post': post, 'message': message})
    else:
        return render(request, 'post_db/reply.html', {'post': post})

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

