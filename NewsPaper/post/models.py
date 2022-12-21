from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse
from author.models import Author
from category.models import Category


class Post(models.Model):
    class PostType(models.TextChoices):
        ARTICLE = 'AR', _('Article')
        NEWS = 'NS', _('News')

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(
        max_length=2, choices=PostType.choices, default=PostType.NEWS)
    time = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, chars=124):
        return self.text[:chars] + '...'

    def __gt__(self, other) -> bool:
        if isinstance(other, Post):
            return self.rating > other.rating
        return NotImplemented

    def __str__(self) -> str:
        return f'Date: {self.time}\nPost author: {self.author}\nPost rating: {self.rating}\nPreview: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
        #return f'/news/{self.id}'

    @property
    def get_post_type(self):
        return dict(self.PostType.choices)[self.post_type]


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PostCounter(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    count_post = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.author.username.username}, date: {self.date}, posts: {self.count_post}'
