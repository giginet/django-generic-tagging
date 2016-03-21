from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.renderers import JSONRenderer
from generic_tagging.api.serializers import TagSerializer, TaggedItemSerializer
from generic_tagging.models import Tag, TaggedItem


class TagViewSet(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    renderer_classes = (JSONRenderer, )


class TaggedItemViewSet(mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = TaggedItemSerializer
    queryset = TaggedItem.objects.all()
    renderer_classes = (JSONRenderer, )
