from django.shortcuts import render, get_object_or_404
from .models import Post
#from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView)

# Create your views here.

# posts=[
#     {
#         'author': 'Spencer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 12, 2019'
#     },
#     {
#         'author': 'Kali Kimball',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 13, 2019'
#     }
# ]


def home(request):
    # context={
    #     'posts':posts 
    # }
    context={
        'posts': Post.objects.all()
    }

    return render(request, 'blog/home.html', context)

#Class based views:

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    #^^These are all from ListView, which is our inherited class
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    #^^These are all from ListView, which is our inherited class
    paginate_by = 2

    # def get_query_set(self):
    #     user = get_object_or_404(User, username=self.kwargs.get())
    #     return Post.objects.filter(author=user).ordery_by('-date_posted')
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html',{'title': 'About'})






