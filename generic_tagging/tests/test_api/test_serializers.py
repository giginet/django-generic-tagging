from django.test.testcases import TestCase
from ...api.serializers import TaggedItemSerializer
from ..factories import TaggedItemFactory


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
