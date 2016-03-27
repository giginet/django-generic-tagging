from django.db import models


class Article(models.Model):
    title = models.CharField('Title', max_length=64)
    body = models.TextField('Body')

    @models.permalink
    def get_absolute_url(self):
        return ('blog_article_detail', (), {'pk': self.pk})

    def __str__(self):
        return self.title
