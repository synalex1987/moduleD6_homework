from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import date
from threading import Thread

from NewsPaper.settings import BASE_URL
from .models import Category, PostCategory, Post, PostCounter


@receiver(pre_save, sender=Post)
def func(sender, instance, **kwargs):
    if (instance._state.adding):
        try:
            post_counter = PostCounter.objects.get(author=instance.author)
            if post_counter.date != date.today():
                post_counter.date = date.today()
                post_counter.count_post = 1
            else:
                post_counter.count_post += 1
            post_counter.save()
        except:
            PostCounter.objects.create(
                author=instance.author, date=date.today(), count_post=1)


@receiver(m2m_changed, sender=PostCategory)
def func(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        Thread(target=send_email_about_new_post,
               args=(instance, )).start()


def send_email_about_new_post(instance):
    post_data = {'title': instance.title, 'text': instance.text, 'url': BASE_URL + instance.get_absolute_url()}
    for cat in instance.category.values():
        for user in Category.objects.get(id=cat['id']).subscribers.all():
            post_data['user'] = user
            html_content = render_to_string('email.html', post_data)
            msg = EmailMultiAlternatives(post_data['title'], html_content,
                                         from_email='nbvwzbaotjrclrbea@gmx.com',
                                         to=[post_data['user'].email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                continue
