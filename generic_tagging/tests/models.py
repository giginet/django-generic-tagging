from django.db import models


class TagTestArticle(models.Model):
    title = models.CharField('Title', max_length=255)

    class Meta:
        app_label = 'generic_tagging'
