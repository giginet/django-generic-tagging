from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from generic_tagging.api.fields import TagField
from ..models import Tag, TaggedItem, TagManager


class TagSerializer(serializers.HyperlinkedModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'label', 'url', 'absolute_url')
        extra_kwargs = {'id': {'read_only': True}}

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        request = self.context.get('request', None)
        if request:
            rep['absolute_url'] = request.build_absolute_uri(rep['absolute_url'])
        return rep

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
