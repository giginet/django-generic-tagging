import factory
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from ..models import Tag, TaggedItem

from .models import TagTestArticle


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    last_name = 'John'
    first_name = 'Doe'
    username = factory.sequence(lambda n: 'username{0}'.format(n))
    email = 'webmaster@example.com'
    password = make_password('password')
    last_login = timezone.now()


class TagTestArticleFactory(factory.DjangoModelFactory):
    class Meta:
        model = TagTestArticle

    title = 'Test article'


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.Sequence(lambda n: 'Tag {}'.format(n))


class TaggedItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = TaggedItem

    tag = factory.SubFactory(TagFactory)
    author = factory.SubFactory(UserFactory)
