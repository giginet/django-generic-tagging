from django.conf.urls import url
from rest_framework import routers
from generic_tagging.api.viewsets import TagViewSet, TaggedItemViewSet

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'tags', TagViewSet)
router.register(r'tagged_items', TaggedItemViewSet)
urlpatterns = router.urls
