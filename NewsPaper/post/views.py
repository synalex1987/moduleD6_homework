from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from threading import Thread

from .models import Post, Category, PostCounter
from .filters import PostFilter
from .forms import PostForm
from author.models import Author
from NewsPaper.settings import MAX_POST_PER_DAY

# Класс для отображения всех постов/новостей


class PostList(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'post_list'
    ordering = ['-time']

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['total'] = Post.objects.all().count
        context['categories'] = Category.objects.all()
        return context


# Класс для отображения детальной информации о поста/новости на отдельной странице
class PostDetail(DetailView):
    model = Post
    template_name = 'post/post_detail.html'
    #template_name = 'post/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


# Класс для отображения постов/новостей по фильтру.
class PostListFiltered(ListView):
    model = Post
    template_name = 'post/search.html'
    context_object_name = 'post_list_filtered'
    ordering = ['-time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        if self.request.user.is_authenticated:
            context['subscriptions'] = Category.objects.all()
            context['your_subscriptions'] = [check_cat for check_cat in context['subscriptions']
                                             if User.objects.get(username=self.request.user) in check_cat.subscribers.all()]
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.add_post',)

    def form_valid(self, form):
        #data = self.request.POST
        if form.instance.author.username == User.objects.get(username=self.request.user):
            '''try:
                Thread(target=send_email_about_new_post,
                       args=(data, )).start()
            except:
                pass'''
            try:
                post_counter = PostCounter.objects.get(
                    author=form.instance.author)
                if post_counter.count_post >= MAX_POST_PER_DAY and post_counter.date == datetime.today().date():
                    return render(self.request, 'stop.html')
            except:
                pass
            return super().form_valid(form)
        return render(self.request, 'form_error.html')


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'post/post_create.html'
    permission_required = ('post.change_post',)

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs.get('pk'))


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'post/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('post.delete_post',)


def send_email_about_new_post(data):
    post_data = {'title': data['title'], 'text': data['text'], }
    for cat in data.getlist('category'):
        for user in Category.objects.get(id=cat).subscribers.all():
            post_data['user'] = user
            html_content = render_to_string(
                'email.html', post_data)
            msg = EmailMultiAlternatives(data['title'], html_content,
                                         from_email='nbvwzbaotjrclrbea@gmx.com',
                                         to=[post_data['user'].email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                continue


# TEST TEST TEST
# Класс для отображения ВСЕХ постов/новостей, а также по фильтру. Для тестирования
class PostListWithFilters(ListView):
    model = Post
    template_name = 'post/test/post_list_with_query.html'
    context_object_name = 'post_list_with_query'
    ordering = ['-time']
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['total'] = Post.objects.all().count
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
