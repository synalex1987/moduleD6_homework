from django.db import models
from django.contrib.auth.models import User
from django.apps import apps


class Author(models.Model):
    rating = models.IntegerField(default=0, null=True)
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, primary_key=True)

    def __str__(self) -> str:
        return f'{self.username.username}'

    def update_rating(self):
        self.rating = 0
        posts = apps.get_model('post', 'Post').objects.filter(author_id=self.username_id, post_type='AR')
        author_comments = apps.get_model('comment', 'Comment').objects.filter(username_id=self.username_id)
        for each in author_comments.values():
            self.rating += each['rating']
        for each in posts.values():
            self.rating += each['rating'] * 3
            user_comments = apps.get_model('comment', 'Comment').objects.filter(post_id=each['id'])
            for comment in user_comments.values():
                if comment['username_id'] != self.username_id:
                    self.rating += comment['rating']
                    
        self.save()
    
    def __gt__(self, other) -> bool:
        if isinstance(other, Author):
            return self.rating > other.rating
        return NotImplemented
    