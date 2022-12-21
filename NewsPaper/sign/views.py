from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .models import BaseRegisterForm
from author.models import Author
from category.models import Category


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'
    template_name = 'sign/signup.html'


class LoginViewPage(LoginView):
    template_name = 'sign/login.html'
    success_url = '/news'


class PersonalPage(LoginRequiredMixin, TemplateView):
    template_name = 'sign/personal.html'
    context_object_name = 'personal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()
        context['subscriptions'] = Category.objects.all()
        context['your_subscriptions'] = [check_cat for check_cat in context['subscriptions']
                                         if User.objects.get(username=self.request.user) in check_cat.subscribers.all()]
        return context


@login_required
def make_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    Author.objects.create(username=user)
    return redirect('/news')


@login_required
def subscriptions_update(request):
    user = User.objects.get(username=request.user)
    for check_cat in Category.objects.all():
        if check_cat.name == request.POST.get(check_cat.name):
            check_cat.subscribers.add(user)
        else:
            check_cat.subscribers.remove(user)

    return redirect('personal')
