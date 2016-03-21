from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers

from ..models import Tag, TaggedItem


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')
        extra_kwargs = {'id': {'read_only': True}}

    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(label=data['label'])
        return tag



class TaggedItemSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    tag = TagSerializer()

    class Meta:
        model = TaggedItem
        fields = (
            'id', 'content_type', 'object_id',
            'author', 'locked', 'created_at',
            'tag'
        )
