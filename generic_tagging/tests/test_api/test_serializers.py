from django.test.testcases import TestCase
from django.contrib.contenttypes.models import ContentType

from generic_tagging.models import TaggedItem, Tag
from generic_tagging.api.serializers import TaggedItemSerializer
from generic_tagging.tests.factories import TaggedItemFactory, UserFactory, TagTestArticle0Factory, TagFactory


class TaggedItemSerializerTestCase(TestCase):
    def test_read(self):
        tagged_item = TaggedItemFactory()
        serializer = TaggedItemSerializer(tagged_item)
        data = serializer.data
        self.assertEqual(data['author'], tagged_item.author.pk)
        self.assertIsNotNone(data['created_at'])
        self.assertEqual(data['object_id'], tagged_item.object_id)
        self.assertEqual(data['content_type'], tagged_item.content_type.pk)
        self.assertFalse(data['locked'])
        self.assertEqual(data['tag']['id'], tagged_item.tag.pk)
        self.assertEqual(data['tag']['label'], tagged_item.tag.label)

    def test_write_with_new_tag(self):
        user = UserFactory()
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)

        tagged_item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()
        serializer = TaggedItemSerializer(data={'author': user.pk, 'object_id': article.pk, 'content_type': ct.pk, 'tag': {'label': 'hoge'}})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        tagged_item = serializer.save()
        self.assertIsNotNone(tagged_item)
        self.assertEqual(TaggedItem.objects.count(), tagged_item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count + 1)

    def test_write_with_exist_tag(self):
        user = UserFactory()
        article = TagTestArticle0Factory()
        ct = ContentType.objects.get_for_model(article)
        tag = TagFactory()

        tagged_item_count = TaggedItem.objects.count()
        tag_count = Tag.objects.count()
        serializer = TaggedItemSerializer(data={'author': user.pk, 'object_id': article.pk, 'content_type': ct.pk, 'tag': {'label': tag.label}})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})

        tagged_item = serializer.save()
        self.assertIsNotNone(tagged_item)
        self.assertEqual(TaggedItem.objects.count(), tagged_item_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count)
