from django.test import TestCase
import requests
from random import randint
from .models import Post, Category


def make_news(amount=30):
    url = 'https://fish-text.ru/get'
    for _ in range(amount):
        r = requests.get(url).json()
        #print(f"Post.objects.create(author_id={randint(1, 2)}, post_type='NS', title={randint(1, 9999)}, text={r['text']}")
        Post.objects.create(author_id=randint(
            1, 2), post_type='NS', title=str(randint(1, 9999)), text=r['text'])


def make_categories(posts=Post.objects.all().values('id')):
    for i in posts:
        p = Post.objects.get(id=i['id'])
        len_cats = Category.objects.all().__len__()
        p.category.set([Category.objects.get(id=randint(1, len_cats)),
                        Category.objects.get(id=randint(1, len_cats))])
