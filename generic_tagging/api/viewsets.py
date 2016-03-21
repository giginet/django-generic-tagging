from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route
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
    renderer_classes = (JSONRenderer,)


class TaggedItemViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = TaggedItemSerializer
    queryset = TaggedItem.objects.all()
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        qs = super().get_queryset()
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        if object_id and content_type:
            qs = qs.filter(object_id=object_id, content_type=content_type)
        return qs

    def list(self, request, *args, **kwargs):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        if not (content_type and object_id):
            return Response('Query parameters must contain content_type and object_id.',
                            status=status.HTTP_400_BAD_REQUEST)
        return super().list(request, *args, **kwargs)


    def create(self, request):
        data = request.data
        if request.user.is_authenticated:
            data['author'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=['patch'])
    def lock(self, request, pk):
        item = self.get_object()
        try:
            item.lock(request.user)
            serializer = TaggedItemSerializer(item)
            return Response(serializer.data)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ValidationError:
            return Response('the tag is already locked',
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['patch'])
    def unlock(self, request, pk):
        item = self.get_object()
        try:
            item.unlock(request.user)
            serializer = TaggedItemSerializer(item)
            return Response(serializer.data)
        except PermissionDenied:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ValidationError:
            return Response('the tag is already unlocked',
                            status=status.HTTP_400_BAD_REQUEST)
