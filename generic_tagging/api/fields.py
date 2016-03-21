from rest_framework import serializers
from generic_tagging.models import Tag


class TagField(serializers.Field):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'label': obj.label
        }

    def to_internal_value(self, data):
        (tag, created) = Tag.objects.get_or_create(label=data['label'])
        return tag
