from rest_framework import viewsets
from generic_tagging.api.serializers import TagSerializer, TaggedItemSerializer
from generic_tagging.models import Tag, TaggedItem


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TaggedItemViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    serializer_class = TaggedItemViewSet
    queryset = TaggedItem.objects.all()
