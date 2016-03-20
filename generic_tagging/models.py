from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)

    class Meta:
        ordering = ('label',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('Tag'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content type'))
    object_id = models.PositiveIntegerField(_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    locked = models.BooleanField(_('Locked'), default=False)
    order = models.IntegerField(_('Order'), default=0, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        ordering = ('order', '-created_at')
        unique_together = ('tag', 'content_type', 'object_id')
        verbose_name = _('Tagged item')
        verbose_name_plural = _('Tagged items')
        permissions = (
            ('lock_tagged_item', 'Can lock tagged item'),
        )
