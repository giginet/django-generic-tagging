from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from generic_tagging.api.fields import TagField
from ..models import Tag, TaggedItem


class ContentObjectSerializer(serializers.Serializer):
    content_type = serializers.SerializerMethodField()
    object_id = serializers.SerializerMethodField(read_only=True)
    str = serializers.SerializerMethodField(read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)

    def get_content_type(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        return ct.pk

    def get_object_id(self, obj):
        return obj.pk

    def get_absolute_url(self, obj):
        if not hasattr(obj, 'get_absolute_url'):
            return None
        request = self.context.get('request', None)
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()

    def get_str(self, obj):
        return str(obj)


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
    content_object = ContentObjectSerializer(read_only=True)
    tag = TagField()

    class Meta:
        model = TaggedItem
        fields = (
            'id', 'content_type', 'object_id', 'content_object',
            'author', 'locked', 'created_at',
            'tag'
        )
