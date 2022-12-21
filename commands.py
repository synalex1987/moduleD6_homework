from django.contrib.auth.models import User
from django.apps import apps

from author.models import Author
from post.models import Post
from comment.models import Comment
from category.models import Category

# 1
user1 = User.objects.create(username='user1')
user2 = User.objects.create(username='user2')

# 2
author1 = Author.objects.create(username=user1)
author2 = Author.objects.create(username=user2)

# 3
Category.objects.create(name='Sport')
Category.objects.create(name='Music')
Category.objects.create(name='3D')
Category.objects.create(name='Blog')

# 4
article1 = Post.objects.create(author=author1, post_type='AR', title='Article1', text='В рамках спецификации современных стандартов, явные признаки победы институционализации, превозмогая сложившуюся непростую экономическую ситуацию, описаны максимально подробно. Есть над чем задуматься: явные признаки победы институционализации будут объединены в целые кластеры себе подобных.')
article2 = Post.objects.create(author=author2, post_type='AR', title='Article2', text='А также элементы политического процесса функционально разнесены на независимые элементы. Есть над чем задуматься: предприниматели в сети интернет и по сей день остаются уделом либералов, которые жаждут быть своевременно верифицированы.')
news = Post.objects.create(author=author1, title='News 1', text='Безусловно, социально-экономическое развитие способствует повышению качества системы обучения кадров, соответствующей насущным потребностям. Как уже неоднократно упомянуто, представители современных социальных резервов будут смешаны с не уникальными данными до степени совершенной неузнаваемости, из-за чего возрастает их статус бесполезности.')

# 5
article1.category.set(Category.objects.filter(name='Sport'))
article2.category.set([Category.objects.get(name='3D'), Category.objects.get(name='Music')])
news.category.set(Category.objects.filter(name='Blog'))

# 6
c1 = Comment.objects.create(post = article1, username = user1, text='comment1')
c2 = Comment.objects.create(post = article2, username = user1, text='comment2')
c3 = Comment.objects.create(post = news, username = user1, text='comment3')
c4 = Comment.objects.create(post = article1, username = user2, text='comment4')
c5 = Comment.objects.create(post = article1, username = user2, text='comment5')
c6 = Comment.objects.create(post = article1, username = user2, text='comment6')
c7 = Comment.objects.create(post = article2, username = user1, text='comment7')

# 7
article1.like()
article2.like()
article2.like()
news.like()
c1.like()
c1.like()
c5.dislike()
c5.dislike()
c6.dislike()
c6.dislike()

# 8
author1.update_rating()
author2.update_rating()

# 9
max(Author.objects.all())

# 10
max(Post.objects.all())

# 11
best_post = max(Post.objects.all())
Comment.objects.filter(post_id=best_post).values('time', 'username', 'rating', 'text')