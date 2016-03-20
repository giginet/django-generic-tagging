from django.db import models


class TagTestArticle(models.Model):
    title = models.CharField('Title')
