from django import template
from ..models import TaggedItem, Tag

register = template.Library()


@register.assignment_tag
def get_tagged_items_for(object):
    '''retrieve tagged items which relative with the specific object.
    :syntax: {% get_tagged_items_for <object> as <variable> %}
    '''
    return TaggedItem.objects.get_for_object(object)


@register.assignment_tag
def get_tags_for(object):
    '''retrieve tags which relative with the specific object.
    :syntax: {% get_tags_for <object> as <variable> %}
    '''
    return Tag.objects.get_for_object(object)
