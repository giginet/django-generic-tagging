from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from generic_tagging.api.fields import TagField
from ..models import Tag, TaggedItem, TagManager


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')
        extra_kwargs = {'id': {'read_only': True}}


class TaggedItemSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    created_at = serializers.DateTimeField(read_only=True)
    tag = TagField()

    class Meta:
        model = TaggedItem
        fields = (
            'id', 'content_type', 'object_id',
            'author', 'locked', 'created_at',
            'tag'
        )
