from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from rest_framework import serializers

from ..models import Tag, TaggedItem

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')

class TaggedItemSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    tag = TagSerializer()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TaggedItem
        fields = (
            'id', 'content_type', 'object_id',
            'author', 'locked', 'created_at', 'tag'
        )

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        User = settings.AUTH_USER_MODEL
        author = User.objects.get(pk=author_data.pk)
        content_object = validated_data.pop('content_object')
        label = validated_data.pop('label')
        tagged_item = TaggedItem.objects.add(label, content_object, author)
        return tagged_item
