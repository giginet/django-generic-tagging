from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import ugettext_lazy as _


class TagManager(models.Manager):
    def get_for_object(self, object):
        '''Get tags which are belonged to the specific object
        :param obj: Object
        '''
        ct = ContentType.objects.get_for_model(object)
        return self.filter(items__content_type=ct, items__object_id=object.pk).distinct()


class TaggedItemManager(models.Manager):
    def add(self, label, object, author):
        '''Add the tag to the specific object.
        If the tag named as 'label' is not exist, it will be created.
        :param label: Tag name
        :param object: Object
        :param author: Author
        '''
        if not author.has_perm('generic_tagging.add_tagged_item', obj=object):
            raise PermissionDenied('The user could not add the label to the object')
        ct = ContentType.objects.get_for_model(object)
        tag = Tag.objects.get_or_create(label)
        tagged_item = self.create(tag=tag,
                                  content_type=ct,
                                  object_id=object.pk,
                                  author=author)
        return tagged_item

    def remove(self, label, object):
        '''Remove the tag from the specific object
        :param label: Tag name
        :param object: Object
        '''
        ct = ContentType.objects.get_for_model(object)
        self.remove(tag__label=label, content_type=ct, object_id=object.pk)

    def clear(self, object):
        '''Clear all tagged item from the object
        :param object: Object
        '''
        ct = ContentType.objects.get_for_model(object)
        self.remove(content_type=ct, object_id=object.pk)

    def get_tag_count(self, object):
        '''Get number of tags which are belonged to the specific object
        :param object:
        :return: number of tags
        '''
        ct = ContentType.objects.get_for_model(object)
        return self.count(content_type=ct, object_id=object.pk)

    @staticmethod
    def swap_order(tagged_item, other_tagged_item):
        '''Swap the orders between two tagged items which are belonged to a same object
        If two tagged items owners are not same, then it will raise `ValidationError`.
        :param tagged_item: Tagged item
        :param other_tagged_item: Another tagged item
        :return:
        '''
        if not (tagged_item.content_type.pk == other_tagged_item.content_type.pk and
                        tagged_item.object_id == other_tagged_item.object_id):
            raise ValidationError('These tags are not belonged to same object')
        temp = tagged_item.order
        tagged_item.order = other_tagged_item.order
        other_tagged_item.order = temp
        tagged_item.save()
        other_tagged_item.save()


class Tag(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)

    objects = TagManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.label


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('Tag'), related_name='items')
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content type'))
    object_id = models.PositiveIntegerField(_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    locked = models.BooleanField(_('Locked'), default=False)
    order = models.IntegerField(_('Order'), default=0, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    objects = TaggedItemManager()

    class Meta:
        ordering = ('order', '-created_at')
        unique_together = ('tag', 'content_type', 'object_id')
        verbose_name = _('Tagged item')
        verbose_name_plural = _('Tagged items')
        permissions = (
            ('lock_tagged_item', 'Can lock tagged item'),
            ('unlock_tagged_item', 'Can unlock tagged item'),
        )

    def __str__(self):
        return '{} {}'.format(str(self.tag), str(self.content_object))

    def lock(self, by_user):
        '''Lock this tag
        If `by_user` doesn't have `lock_tagged_item` permission, then it will raise `PermissionDenied` exception
        :param by_user: User who attempt to lock
        '''
        if self.locked:
            raise ValidationError('''The tagged item is already locked''')
        if not by_user.has_perm('lock_tagged_item', obj=self):
            raise PermissionDenied('''The user doesn't have lock_tagged_item permission''')
        self.locked = True
        self.save()

    def unlock(self, by_user):
        '''Unlock this tag
        If `by_user` doesn't have `unlock_tagged_item` permission, then it will raise `PermissionDenied` exception
        :param by_user:
        '''
        if not self.locked:
            raise ValidationError('''The tagged item is already unlocked''')
        if not by_user.has_perm('unlock_tagged_item', obj=self):
            raise PermissionDenied('''The user doesn't have unlock_tagged_item permission''')
        self.locked = False
        self.save()
