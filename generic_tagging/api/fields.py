from django.core.exceptions import ValidationError
from rest_framework import serializers
from generic_tagging.models import Tag


class TagField(serializers.Field):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'label': obj.label
        }

    def to_internal_value(self, data):
        if isinstance(data, str):
            key = {'label': data}
        elif isinstance(data, dict):
            if 'label' in data:
                key = {'label': data['label']}
            else:
                raise ValidationError('tag parameter must contains label')
        (tag, created) = Tag.objects.get_or_create(**key)
        return tag
